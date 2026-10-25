"""
Matches each "...Response" event to its corresponding "...Request" event(s)
using localTransactionId + (clientNumber / swn / identifier), then extracts
the *request* payload and saves it under:

    output_<timestamp>/<response_eventName>/<resultCode>_<message>/N_<idValue>.xml

Duplicate payloads (structurally identical, ignoring volatile fields like
auditId/correlationId/requestDateTime/transactionId) are written only once
per folder.

Reads every *.json file under INPUT_DIR (one JSON object per line, Splunk
export format), where each record looks like:

    {"result": {"eventName": "...", "_raw": "...", "localTransactionId": "..."}}
"""

import copy
import glob
import json
import os
import re
from collections import defaultdict
from datetime import datetime
import xml.etree.ElementTree as ET

# Folder containing the Splunk export .json files (one JSON object per line).
INPUT_DIR = "input/20260810"

# All output goes under <project_root>/output_<run_timestamp>/
OUTPUT_DIR_BASE = "output-20260810"

# Responses with these localTransactionId values are automation-generated
# noise - never try to match them to a request. Their details are logged to
# Automation_Generated_Responses_Ignored.txt instead.
IGNORED_LOCAL_TXN_IDS = {"fb43edd1-87f3-5c6e-9d0e-302f62e6c218"}

# Fields whose values are expected to differ per-call even when the
# meaningful payload is otherwise identical - ignored when comparing
# payloads for uniqueness.
VOLATILE_FIELD_NAMES = {"auditId", "correlationId", "requestDateTime", "requestedDateTime", "transactionId"}

# --- Regex extraction of the XML body out of the raw log line ---
# The _raw field has a log prefix (timestamp, thread, log level, etc.) before
# the XML starts, and the element that would normally declare
# xmlns:wmb="..." lives on a parent element that isn't captured in the log
# line. So rather than parsing the <wmb:...> wrapper directly, we pull the
# line. So rather than parsing the <wmb:...> wrapper directly, we pull the
# inner content out via regex; that inner content is typically a
# self-contained, self-namespaced element that parses fine on its own.
COMPLEX_CONTENT_RE = re.compile(
    r"<wmb:complexContent[^>]*>(?P<body>.*)</wmb:complexContent>",
    re.DOTALL,
)


def extract_complex_content_raw(raw_value: str):
    """Pull the raw XML text found between <wmb:complexContent> and </wmb:complexContent>."""
    match = COMPLEX_CONTENT_RE.search(raw_value)
    if not match:
        return None
    return match.group("body").strip()


def parse_complex_content(complex_content_raw):
    """Try to parse the extracted complexContent text as XML. Returns the
    Element, or None if it can't be parsed on its own."""
    if not complex_content_raw:
        return None
    try:
        return ET.fromstring(complex_content_raw)
    except ET.ParseError:
        return None


def local_name(tag: str) -> str:
    """Strip the '{namespace-uri}' prefix ElementTree adds to namespaced tags."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def find_by_local_name(elem, name: str):
    """Find the first descendant (or self) element whose tag matches `name`,
    ignoring any namespace prefix/URI."""
    if elem is None:
        return None
    for node in elem.iter():
        if local_name(node.tag) == name:
            return node
    return None


def find_direct_child_by_local_name(elem, name: str):
    """Find the first DIRECT child (not descendant) whose tag matches `name`."""
    if elem is None:
        return None
    for child in list(elem):
        if local_name(child.tag) == name:
            return child
    return None


def get_first_value_by_local_names(elem, names):
    """Try each candidate tag name in order, return the first non-empty text
    value found anywhere under elem."""
    for name in names:
        found = find_by_local_name(elem, name)
        if found is not None and found.text and found.text.strip():
            return found.text.strip()
    return None


def get_id_value(elem):
    """clientNumber, else swn, else identifier - in that priority order."""
    return get_first_value_by_local_names(elem, ["clientNumber", "swn", "identifier"])


def get_result_code_value(elem):
    """resultCode, else code."""
    return get_first_value_by_local_names(elem, ["result", "resultCode"])


def get_message_value(elem):
    return get_first_value_by_local_names(elem, ["message"])


def get_local_txn_id_value(elem):
    return get_first_value_by_local_names(elem, ["localTransactionId"])


# --- Full-raw-text extraction ---
# Fields like the service result/message live in a HEADER section of the
# XML (e.g. <out8:serviceResult><out8:result>...</out8:result></out8:serviceResult>),
# which sits OUTSIDE <wmb:complexContent> - so parsing just the complexContent
# body (as done above) never finds them. Rather than trying to parse the
# entire raw XML as a tree (which runs into the same unbound-namespace-prefix
# problem as the wmb: wrapper), we scan the raw text directly with regex,
# matching on local tag name only and ignoring whatever prefix is used
# (out8:, wmb:, app:, or none). This also works for id values whether they
# happen to live in the header or the body.

def extract_tag_text_from_raw(raw_text: str, local_tag_name: str):
    """Find the first LEAF <[prefix:]local_tag_name ...>...</[prefix:]local_tag_name>
    anywhere in raw_text and return its trimmed inner text, or None.

    "Leaf" means the content between the open and close tag contains no
    further '<' characters - i.e. it's plain text, not a wrapper around
    other elements. This matters because it's common for a container
    element to share the same local name as one of its own descendants
    (e.g. an outer <ns3:result> wrapping a <ns3:message> and an inner
    <ns3:result>52003</ns3:result> holding the actual code). Without the
    leaf restriction, a non-greedy match starting at the outer tag would
    incorrectly stop at the first closing tag it finds - which can be the
    INNER element's closing tag, since it shares the same name - producing
    a garbled result that spans across both elements.
    """
    pattern = re.compile(
        r"<(?:[\w.-]+:)?" + re.escape(local_tag_name) + r"(?:\s[^>]*)?>"
        r"(?P<value>[^<]*)"
        r"</(?:[\w.-]+:)?" + re.escape(local_tag_name) + r"\s*>"
    )
    match = pattern.search(raw_text)
    if not match:
        return None
    value = match.group("value").strip()
    return value or None


def get_first_tag_value_from_raw(raw_text: str, local_tag_names):
    """Try each candidate tag name in order against the full raw text,
    returning the first non-empty match found."""
    if not raw_text:
        return None
    for name in local_tag_names:
        value = extract_tag_text_from_raw(raw_text, name)
        if value:
            return value
    return None


def sanitize_name(name: str) -> str:
    """Make a string safe to use as a folder/file name."""
    if not name:
        return "unknown"
    safe = re.sub(r'[<>:"/\\|?*]', "_", name.strip())
    safe = re.sub(r"\s+", "_", safe)
    return safe or "unknown"


# --- Payload canonicalization (for uniqueness), mirroring the same
# volatile-field-aware approach used elsewhere in this project ---

def get_direct_text(elem: ET.Element) -> str:
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in list(elem):
        if child.tail:
            parts.append(child.tail)
    return " ".join("".join(parts).split())


def remove_volatile_fields(elem: ET.Element):
    """Blank out volatile-named elements anywhere in the tree. Mutates in
    place - always call on a deep copy."""
    nodes_to_clear = [node for node in elem.iter() if local_name(node.tag) in VOLATILE_FIELD_NAMES]
    for node in nodes_to_clear:
        for child in list(node):
            node.remove(child)
        node.text = "__IGNORED__"


def canonical_node_signature(elem: ET.Element) -> dict:
    attributes = sorted(
        ({"Name": local_name(name), "Value": value} for name, value in elem.attrib.items()),
        key=lambda a: a["Name"],
    )
    children = [canonical_node_signature(child) for child in list(elem)]
    return {
        "Name": local_name(elem.tag),
        "Text": get_direct_text(elem),
        "Attributes": attributes,
        "Children": children,
    }


def get_canonical_key_for_xml(elem: ET.Element) -> str:
    elem_copy = copy.deepcopy(elem)
    remove_volatile_fields(elem_copy)
    signature = canonical_node_signature(elem_copy)
    return "XML::" + json.dumps(signature, separators=(",", ":"))


def xml_elem_to_native(elem: ET.Element):
    """Convert an XML element into a plain dict/list/str structure, grouping
    same-named children together (mirrors Convert-XmlNodeToNativeObject)."""
    children = list(elem)
    if not children:
        return get_direct_text(elem)

    grouped = defaultdict(list)
    for child in children:
        grouped[local_name(child.tag)].append(xml_elem_to_native(child))

    result = {}
    for key in sorted(grouped.keys()):
        values = grouped[key]
        result[key] = values[0] if len(values) == 1 else values
    return result


def remove_volatile_fields_from_object(value):
    if isinstance(value, dict):
        result = {}
        for key in sorted(value.keys()):
            if key in VOLATILE_FIELD_NAMES:
                result[key] = "__IGNORED__"
            else:
                result[key] = remove_volatile_fields_from_object(value[key])
        return result
    if isinstance(value, list):
        return [remove_volatile_fields_from_object(v) for v in value]
    return value


def get_canonical_key_for_json_obj(payload_dict) -> str:
    cleaned = remove_volatile_fields_from_object(payload_dict)
    return "JSON::" + json.dumps(cleaned, sort_keys=True, separators=(",", ":"))


def build_soap_envelope(body_xml: str) -> str:
    """Wrap the extracted body XML in a SOAP envelope, same header structure
    used in the other extraction script."""
    return f"""<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Header>
    <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
      <wsse:UsernameToken>
        <wsse:Username>curamsystemuser</wsse:Username>
        <wsse:Password>password</wsse:Password>
      </wsse:UsernameToken>
    </wsse:Security>
  </soapenv:Header>
  <soapenv:Body>
{body_xml}
  </soapenv:Body>
</soapenv:Envelope>"""


def is_json_payload(elem) -> bool:
    """Mirrors Test-IsJsonPayloadBody: true if the body's root element local
    name is 'JSON'."""
    return elem is not None and local_name(elem.tag) == "JSON"


def get_json_payload_object(elem):
    """Mirrors Get-JsonPayloadObject: expects <JSON><Data><ActualPayload>...
    Returns (root_local_name, native_value_dict) or None if not found."""
    data_elem = find_direct_child_by_local_name(elem, "Data")
    if data_elem is None:
        return None
    children = list(data_elem)
    if not children:
        return None
    payload_node = children[0]
    return local_name(payload_node.tag), xml_elem_to_native(payload_node)


# --- Loading records from every input file ---

def load_records(input_dir):
    """Read every *.json file under input_dir and split records into
    request/response lists, extracting the fields needed for matching."""
    requests = []
    responses = []

    input_files = sorted(glob.glob(os.path.join(input_dir, "*.json")))
    if not input_files:
        return requests, responses, input_files

    for input_file in input_files:
        file_label = os.path.basename(input_file)
        with open(input_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                result_obj = record.get("result") or {}
                event_name = result_obj.get("eventName")
                if not event_name:
                    continue

                raw_value = result_obj.get("_raw")
                if not raw_value:
                    continue

                complex_content_raw = extract_complex_content_raw(raw_value)
                complex_content_elem = parse_complex_content(complex_content_raw)

                # These fields can live in the header OR the body of the raw
                # XML, so we scan the full raw_value text rather than just
                # the complexContent body.
                local_txn_id = (
                    result_obj.get("localTransactionId")
                    or record.get("localTransactionId")
                    or get_first_tag_value_from_raw(raw_value, ["localTransactionId"])
                )
                id_value = get_first_tag_value_from_raw(raw_value, ["clientNumber", "swn", "identifier"])

                entry = {
                    "file_label": file_label,
                    "line_num": line_num,
                    "event_name": event_name,
                    "local_txn_id": local_txn_id,
                    "id_value": id_value,
                    "raw_value": raw_value,
                    "complex_content_raw": complex_content_raw,
                    "complex_content_elem": complex_content_elem,
                }

                if "Response" in event_name:
                    entry["result_code"] = get_first_tag_value_from_raw(raw_value, ["resultCode", "result"])
                    entry["message"] = get_first_tag_value_from_raw(raw_value, ["message"])
                    responses.append(entry)
                elif "Request" in event_name:
                    requests.append(entry)
                # Records whose eventName contains neither "Request" nor
                # "Response" aren't relevant to this matching task - skipped.

    return requests, responses, input_files


def build_request_index(requests):
    """Index requests by localTransactionId, for fast lookup during matching."""
    index = defaultdict(list)
    for req in requests:
        if req["local_txn_id"]:
            index[req["local_txn_id"]].append(req)
    return index


def find_matching_requests(response, requests_by_txn):
    """Requests sharing the response's localTransactionId, further filtered
    by id_value (clientNumber/swn/identifier) when both sides have one."""
    txn_id = response["local_txn_id"]
    if not txn_id:
        return []

    candidates = requests_by_txn.get(txn_id, [])
    if response["id_value"]:
        candidates = [
            req for req in candidates
            if not req["id_value"] or req["id_value"] == response["id_value"]
        ]
    return candidates


def save_payload(output_dir, response, request, file_counters, seen_keys_by_folder):
    """Write the request's payload under
    output_dir/<response_event_name>/<resultCode>_<message>/N_<idValue>.(xml|json),
    skipping it if an identical (canonicalized) payload was already written
    to that same folder."""
    elem = request["complex_content_elem"]
    raw = request["complex_content_raw"]

    if not raw:
        return None  # nothing to save

    event_folder = sanitize_name(response["event_name"])
    result_code = response.get("result_code") or "unknown_result"
    message = response.get("message") or "unknown_message"
    result_folder = sanitize_name(f"{result_code}_{message}")

    folder_path = os.path.join(output_dir, event_folder, result_folder)

    # Decide format + canonical key + text to write
    if is_json_payload(elem):
        payload_info = get_json_payload_object(elem)
        if payload_info is not None:
            root_name, native_value = payload_info
            canonical_key = get_canonical_key_for_json_obj({root_name: native_value})
            payload_text = json.dumps({root_name: native_value}, indent=2)
            extension = "json"
        else:
            # Couldn't pull out JSON/Data/<payload> - fall back to raw text.
            canonical_key = "RAW::" + " ".join(raw.split())
            payload_text = raw
            extension = "xml"
    elif elem is not None:
        canonical_key = get_canonical_key_for_xml(elem)
        payload_text = raw
        extension = "xml"
    else:
        # Body didn't parse as standalone XML - best-effort dedup on raw text.
        canonical_key = "RAW::" + " ".join(raw.split())
        payload_text = raw
        extension = "xml"

    seen_keys = seen_keys_by_folder[folder_path]
    if canonical_key in seen_keys:
        return None  # duplicate - skip writing
    seen_keys.add(canonical_key)

    os.makedirs(folder_path, exist_ok=True)
    next_index = file_counters.get(folder_path, 0) + 1
    file_counters[folder_path] = next_index

    id_value = request.get("id_value")
    if id_value:
        file_name = f"{next_index}_{sanitize_name(id_value)}.{extension}"
    else:
        file_name = f"{next_index}.{extension}"

    file_path = os.path.join(folder_path, file_name)

    # Wrap XML bodies in the SOAP envelope before writing. JSON payloads are
    # written as plain JSON - a SOAP envelope doesn't apply there.
    text_to_write = build_soap_envelope(payload_text) if extension == "xml" else payload_text

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text_to_write)

    return file_path


def write_ignored_responses_log(output_dir: str, ignored_responses) -> str:
    """Write details of responses whose localTransactionId is in
    IGNORED_LOCAL_TXN_IDS - these are skipped entirely from matching."""
    lines = []
    for response in ignored_responses:
        lines.append("=" * 100)
        lines.append(f"RESPONSE: {response['file_label']} : Line {response['line_num']}")
        lines.append(f"  eventName          : {response['event_name']}")
        lines.append(f"  localTransactionId : {response['local_txn_id']}")
        lines.append(f"  idValue            : {response['id_value']}")
        lines.append(f"  resultCode/result  : {response.get('result_code')}")
        lines.append(f"  message            : {response.get('message')}")
        lines.append("  --- raw _raw ---")
        lines.append("  " + (response["raw_value"] or "").replace("\n", "\n  "))
        lines.append("")

    os.makedirs(output_dir, exist_ok=True)
    log_path = os.path.join(output_dir, "Automation_Generated_Responses_Ignored.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return log_path


def build_comparison_report(output_dir: str, responses, requests_by_txn) -> str:
    """Write a plain-text report showing each response's extracted fields and
    raw XML alongside its matched request(s), so matching/extraction can be
    eyeballed and verified. Includes unmatched responses too, for
    troubleshooting."""
    lines = []
    for response in responses:
        candidates = find_matching_requests(response, requests_by_txn)

        lines.append("=" * 100)
        lines.append(f"RESPONSE: {response['file_label']} : Line {response['line_num']}")
        lines.append(f"  eventName          : {response['event_name']}")
        lines.append(f"  localTransactionId : {response['local_txn_id']}")
        lines.append(f"  idValue            : {response['id_value']}")
        lines.append(f"  resultCode/code    : {response.get('result_code')}")
        lines.append(f"  message            : {response.get('message')}")
        lines.append("  --- raw _raw ---")
        lines.append("  " + (response["raw_value"] or "").replace("\n", "\n  "))
        lines.append("")

        if not candidates:
            lines.append("  >>> NO MATCHING REQUEST FOUND <<<")
        else:
            for i, request in enumerate(candidates, start=1):
                lines.append(f"  MATCHED REQUEST #{i}: {request['file_label']} : Line {request['line_num']}")
                lines.append(f"    eventName          : {request['event_name']}")
                lines.append(f"    localTransactionId : {request['local_txn_id']}")
                lines.append(f"    idValue            : {request['id_value']}")
                lines.append("    --- raw _raw ---")
                lines.append("    " + (request["raw_value"] or "").replace("\n", "\n    "))
                lines.append("")
        lines.append("")

    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "match_comparison.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return report_path


def main():
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{OUTPUT_DIR_BASE}_{run_timestamp}"

    requests, responses, input_files = load_records(INPUT_DIR)
    if not input_files:
        print(f"No .json files found in '{INPUT_DIR}'.")
        return

    print(f"Loaded {len(requests)} request record(s) and {len(responses)} response record(s) "
          f"from {len(input_files)} file(s).")

    ignored_responses = [r for r in responses if r["local_txn_id"] in IGNORED_LOCAL_TXN_IDS]
    responses = [r for r in responses if r["local_txn_id"] not in IGNORED_LOCAL_TXN_IDS]

    if ignored_responses:
        ignored_log_path = write_ignored_responses_log(output_dir, ignored_responses)
        print(f"Ignored {len(ignored_responses)} automation-generated response(s) "
              f"(logged to: {ignored_log_path})")

    requests_by_txn = build_request_index(requests)

    comparison_report_path = build_comparison_report(output_dir, responses, requests_by_txn)
    print(f"Comparison report written to: {comparison_report_path}")
    print()

    file_counters = {}  # next file index, per output folder
    seen_keys_by_folder = defaultdict(set)  # canonical keys already written, per output folder

    matched_response_count = 0
    unmatched_response_count = 0
    files_written = 0

    for response in responses:
        candidates = find_matching_requests(response, requests_by_txn)

        label = (f"{response['file_label']} : Line {response['line_num']}"
                  f" (eventName={response['event_name']}, "
                  f"localTransactionId={response['local_txn_id']}, "
                  f"idValue={response['id_value']})")

        if not candidates:
            print(f"[No match] {label}")
            unmatched_response_count += 1
            continue

        matched_response_count += 1
        print(f"[Matched {len(candidates)} request(s)] {label}")

        for request in candidates:
            file_path = save_payload(output_dir, response, request, file_counters, seen_keys_by_folder)
            if file_path:
                files_written += 1
                print(f"  -> wrote {file_path}")
            else:
                print(f"  -> duplicate payload, skipped (from {request['file_label']} : Line {request['line_num']})")

    print()
    print(f"Responses matched: {matched_response_count}")
    print(f"Responses with no matching request: {unmatched_response_count}")
    print(f"Unique payload files written: {files_written}")
    print(f"Output folder: {output_dir}")


if __name__ == "__main__":
    main()