import json
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
from lxml import etree


def _sniff_format(body: str):
    """
    Return 'xml', 'json', or None based on the first non-whitespace
    character of the given string. Shared by _detect_format_from_content
    (request payload templates) and detect_response_type (HTTP responses).
    """
    stripped = body.strip()
    if stripped.startswith("<"):
        return "xml"
    if stripped.startswith("{") or stripped.startswith("["):
        return "json"
    return None


def _is_inline_payload(value: str) -> bool:
    """
    Decide whether a PAYLOAD cell value is literal JSON/XML content
    rather than a file path, based on its first non-whitespace character.
    """
    return _sniff_format(value) is not None


def _detect_format_from_content(payload_string: str) -> str:
    fmt = _sniff_format(payload_string)
    if fmt is None:
        raise ValueError(
            f"Unable to determine payload format from content, "
            f"starts with: {payload_string.strip()[:50]!r}"
        )
    return fmt


def _escape_value(value: str, fmt: str) -> str:
    if fmt == "xml":
        return xml_escape(str(value))
    elif fmt == "json":
        # json.dumps wraps in quotes; strip them since we're inserting into existing quotes
        return json.dumps(str(value))[1:-1]
    return str(value)


def parse_validate_data(raw_value: str) -> dict:
    """
    Parse the VALIDATE_DATA CSV cell into a dict.

    Handles the case where the JSON is wrapped in a literal single quote,
    e.g. the CSV cell contains: '{"CelsiusToFahrenheitResult":"68"}'
    (with the ' characters actually part of the string).
    """
    if not raw_value:
        return {}
    cleaned = raw_value.strip()

    # Strip one layer of wrapping single quotes if present
    if cleaned.startswith("'") and cleaned.endswith("'"):
        cleaned = cleaned[1:-1]

    return json.loads(cleaned)

def resolve_query_params(query_string: str, placeholder_values: dict) -> dict:
    """
    Substitute placeholder tokens into a QUERY_STRING template (a JSON-object
    string, e.g. '{"param1":"VALUE1"}') and parse the result into a dict.

    Mirrors resolve_payload's substitute-then-parse approach, but returns a
    dict instead of a raw string since query params are used as a dict
    downstream (api_context.apim.query_params).
    """
    resolved = query_string
    for key, value in placeholder_values.items():
        resolved = resolved.replace(f"{key}", _escape_value(value, "json"))

    return parse_validate_data(resolved)


# --------------------------------------------------------------------------
# Structural (tag/key-name) replacement - namespace-agnostic for XML
# --------------------------------------------------------------------------

def _local_name(tag) -> str:
    """
    Strip namespace from an lxml tag, e.g. '{http://ns}Foo' -> 'Foo'.
    lxml comments/PIs surface a non-string callable as .tag; stringify
    those harmlessly so they just fail to match anything.
    """
    if not isinstance(tag, str):
        return str(tag)
    return tag.split("}", 1)[-1] if "}" in tag else tag


def replace_xml_values(xml_input: str, replacements: dict, case_sensitive: bool = True) -> str:
    """
    Replace the text content of any XML element whose LOCAL tag name
    (namespace ignored) matches a key in `replacements`. Also replaces
    matching attribute values by local attribute name.

    Uses lxml, which preserves the source document's original namespace
    prefixes on serialization.

    Keys in `replacements` with no match anywhere in the payload are
    silently ignored - no exception is raised.
    """
    lookup = replacements if case_sensitive else {k.lower(): v for k, v in replacements.items()}

    root = etree.fromstring(xml_input.encode("utf-8"))

    for elem in root.iter():
        tag_name = _local_name(elem.tag)
        key = tag_name if case_sensitive else tag_name.lower()
        if key in lookup:
            elem.text = str(lookup[key])

        for attr_name in list(elem.attrib.keys()):
            attr_local = _local_name(attr_name)
            attr_key = attr_local if case_sensitive else attr_local.lower()
            if attr_key in lookup:
                elem.set(attr_name, str(lookup[attr_key]))

    return etree.tostring(root, encoding="unicode")


def replace_json_values(json_input, replacements: dict, case_sensitive: bool = True):
    """
    Recursively replace the value of any key (at any depth, including
    inside lists/nested objects) that matches a key in `replacements`.

    Keys in `replacements` with no match anywhere in the payload are
    silently ignored - no exception is raised.

    Args:
        json_input: JSON string OR an already-parsed dict/list.

    Returns:
        str (pretty-printed) if json_input was a string, else dict/list.
    """
    is_string_input = isinstance(json_input, str)
    data = json.loads(json_input) if is_string_input else json.loads(json.dumps(json_input))

    lookup = replacements if case_sensitive else {k.lower(): v for k, v in replacements.items()}

    def _walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                match_key = key if case_sensitive else key.lower()
                if match_key in lookup:
                    node[key] = lookup[match_key]
                else:
                    _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(data)
    return json.dumps(data, indent=2) if is_string_input else data


def resolve_payload(template_path_or_content, values: dict, case_sensitive: bool = True) -> str:
    """
    Resolve a payload template into its final string form, substituting
    placeholder values.

    Accepts either:
    - a Path to a .json/.xml template file, or
    - a str containing the raw JSON/XML payload content directly.

    `values` keys can be given in two styles, freely mixed in the same dict:

    - Curly-brace placeholder tokens, e.g. "{celsius}": "35.5"
      -> literal text substitution (str.replace), escaped appropriately for
         the payload format (XML entity escaping / JSON string escaping).
         This is the original template-token convention and its behavior
         is unchanged.

    - Plain field/tag names, e.g. "AccountNumber": "12345678"
      -> structural replacement: matches XML elements by LOCAL tag name
         (namespace ignored) or attribute name, or JSON object keys at any
         depth, via replace_xml_values / replace_json_values.

    Any key (either style) with no match anywhere in the payload is
    silently ignored - no exception is raised for unmatched fields.
    """
    if isinstance(template_path_or_content, Path):
        payload_string = template_path_or_content.read_text(encoding="utf-8")
        suffix = template_path_or_content.suffix.lower()
        fmt = "xml" if suffix == ".xml" else "json" if suffix == ".json" else None

        if fmt is None:
            raise ValueError(f"Unsupported template type: {suffix}")
    else:
        payload_string = template_path_or_content
        fmt = _detect_format_from_content(payload_string)

    placeholder_values = {k: v for k, v in values.items() if k.startswith("{") and k.endswith("}")}
    field_values = {k: v for k, v in values.items() if k not in placeholder_values}

    # 1. Literal {placeholder} substitution - existing convention, escaped.
    for key, value in placeholder_values.items():
        payload_string = payload_string.replace(key, _escape_value(value, fmt))

    # 2. Structural field/tag-name replacement, namespace-agnostic for XML.
    if field_values:
        if fmt == "xml":
            payload_string = replace_xml_values(payload_string, field_values, case_sensitive=case_sensitive)
        else:
            payload_string = replace_json_values(payload_string, field_values, case_sensitive=case_sensitive)

    if fmt == "xml":
        etree.fromstring(payload_string.encode("utf-8"))
    else:
        json.loads(payload_string)

    return payload_string


def detect_response_type(response) -> str:
    """
    Determine whether a response body is XML or JSON, without relying on
    the request payload's file extension (which doesn't exist for GET
    requests, or may not match the response type).

    Priority:
    1. Content-Type header (most reliable, when the API sets it correctly)
    2. Content sniffing - first non-whitespace character of the body
    3. Raises if neither approach can determine the type

    Returns "xml" or "json".
    """
    content_type = response.headers.get("Content-Type", "").lower()

    if "json" in content_type:
        return "json"
    if "xml" in content_type:
        return "xml"

    # Content-Type missing, generic (e.g. "text/plain"), or misreported by
    # the API - fall back to sniffing the actual body content.
    body = response.text().strip() if callable(response.text) else response.text.strip()

    fmt = _sniff_format(body)
    if fmt is None:
        raise ValueError(
            f"Unable to determine response type. Content-Type='{content_type}', "
            f"body starts with: {body[:50]!r}"
        )
    return fmt

# import json
# from pathlib import Path
# from xml.sax.saxutils import escape as xml_escape
# from lxml import etree
#
#
# def _sniff_format(body: str):
#     """
#     Return 'xml', 'json', or None based on the first non-whitespace
#     character of the given string. Shared by _detect_format_from_content
#     (request payload templates) and detect_response_type (HTTP responses).
#     """
#     stripped = body.strip()
#     if stripped.startswith("<"):
#         return "xml"
#     if stripped.startswith("{") or stripped.startswith("["):
#         return "json"
#     return None
#
#
# def _is_inline_payload(value: str) -> bool:
#     """
#     Decide whether a PAYLOAD cell value is literal JSON/XML content
#     rather than a file path, based on its first non-whitespace character.
#     """
#     return _sniff_format(value) is not None
#
#
# def _detect_format_from_content(payload_string: str) -> str:
#     fmt = _sniff_format(payload_string)
#     if fmt is None:
#         raise ValueError(
#             f"Unable to determine payload format from content, "
#             f"starts with: {payload_string.strip()[:50]!r}"
#         )
#     return fmt
#
#
# def _escape_value(value: str, fmt: str) -> str:
#     if fmt == "xml":
#         return xml_escape(str(value))
#     elif fmt == "json":
#         # json.dumps wraps in quotes; strip them since we're inserting into existing quotes
#         return json.dumps(str(value))[1:-1]
#     return str(value)
#
#
# def parse_validate_data(raw_value: str) -> dict:
#     """
#     Parse the VALIDATE_DATA CSV cell into a dict.
#
#     Handles the case where the JSON is wrapped in a literal single quote,
#     e.g. the CSV cell contains: '{"CelsiusToFahrenheitResult":"68"}'
#     (with the ' characters actually part of the string).
#     """
#     if not raw_value:
#         return {}
#     cleaned = raw_value.strip()
#
#     # Strip one layer of wrapping single quotes if present
#     if cleaned.startswith("'") and cleaned.endswith("'"):
#         cleaned = cleaned[1:-1]
#
#     return json.loads(cleaned)
#
# def resolve_query_params(query_string: str, placeholder_values: dict) -> dict:
#     """
#     Substitute placeholder tokens into a QUERY_STRING template (a JSON-object
#     string, e.g. '{"param1":"VALUE1"}') and parse the result into a dict.
#
#     Mirrors resolve_payload's substitute-then-parse approach, but returns a
#     dict instead of a raw string since query params are used as a dict
#     downstream (api_context.apim.query_params).
#     """
#     resolved = query_string
#     for key, value in placeholder_values.items():
#         resolved = resolved.replace(f"{key}", _escape_value(value, "json"))
#
#     return parse_validate_data(resolved)
#
#
# def resolve_payload(template_path_or_content, values: dict) -> str:
#     """
#     Resolve a payload template into its final string form, substituting
#     placeholder values.
#
#     Accepts either:
#     - a Path to a .json/.xml template file, or
#     - a str containing the raw JSON/XML payload content directly.
#     """
#     if isinstance(template_path_or_content, Path):
#         payload_string = template_path_or_content.read_text(encoding="utf-8")
#         suffix = template_path_or_content.suffix.lower()
#         fmt = "xml" if suffix == ".xml" else "json" if suffix == ".json" else None
#
#         if fmt is None:
#             raise ValueError(f"Unsupported template type: {suffix}")
#     else:
#         payload_string = template_path_or_content
#         fmt = _detect_format_from_content(payload_string)
#
#     for key, value in values.items():
#         payload_string = payload_string.replace(f"{key}", _escape_value(value, fmt))
#
#     if fmt == "xml":
#         etree.fromstring(payload_string.encode("utf-8"))
#     else:
#         json.loads(payload_string)
#
#     return payload_string
#
#
# def detect_response_type(response) -> str:
#     """
#     Determine whether a response body is XML or JSON, without relying on
#     the request payload's file extension (which doesn't exist for GET
#     requests, or may not match the response type).
#
#     Priority:
#     1. Content-Type header (most reliable, when the API sets it correctly)
#     2. Content sniffing - first non-whitespace character of the body
#     3. Raises if neither approach can determine the type
#
#     Returns "xml" or "json".
#     """
#     content_type = response.headers.get("Content-Type", "").lower()
#
#     if "json" in content_type:
#         return "json"
#     if "xml" in content_type:
#         return "xml"
#
#     # Content-Type missing, generic (e.g. "text/plain"), or misreported by
#     # the API - fall back to sniffing the actual body content.
#     body = response.text().strip() if callable(response.text) else response.text.strip()
#
#     fmt = _sniff_format(body)
#     if fmt is None:
#         raise ValueError(
#             f"Unable to determine response type. Content-Type='{content_type}', "
#             f"body starts with: {body[:50]!r}"
#         )
#     return fmt