import re
import sys
import textwrap
from pathlib import Path
from xml.etree import ElementTree as ET

# Environment setup
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "tools"

PAYLOAD_DIR = PROJECT_ROOT / "apps" / "services" / "integration_soap" / "payload_data"/ "template"
PAYLOAD_DATA_INIT = PAYLOAD_DIR / "__init__.py"
PAYLOAD_SETUP_FILE = PROJECT_ROOT / "utils" / "api_utils" / "helper" / "payload_setup.py"
COMPARISON_ROOT = PROJECT_ROOT / "tests" / "api_test" / "soap_api" / "comparison_testing"/ "template"

ALLURE_TESTCASE_URL = "https://msd-jira-cloud.atlassian.net/browse/API-XXXX"
MSD_SUB_ENV = "d11"
DEFAULT_CONDITION = "successful_response"

_LABEL_SC_RE = re.compile(r"^SC(\d+)(?:([vV])(\d+))?:$", re.IGNORECASE)
_ENVELOPE_START_RE = re.compile(r"<(?P<prefix>[A-Za-z]\w*):Envelope[^>]*>.*?</(?P=prefix):Envelope>", re.S)
_BATCH_FILE_RE = re.compile(r"batch(\d+)", re.IGNORECASE)


def parse_payload_file(xml_path):
    # parse the payload from the batchxxx.xml file
    text = Path(xml_path).read_text(encoding="utf-8")

    records = {}
    current_label = None
    current_segment = []

    for line in text.splitlines():
        stripped = line.strip()

        if _LABEL_SC_RE.match(stripped):
            if current_label is not None:
                _add_segment(records, current_label, current_segment)

            current_label = stripped[:-1]
            current_segment = []

        elif current_label is not None:
            current_segment.append(line)

    if current_label is not None:
        _add_segment(records, current_label, current_segment)

    return list(records.values())


def _add_segment(records, label, segment_lines):
    segment = "\n".join(segment_lines)
    matches = list(_ENVELOPE_START_RE.finditer(segment))
    if not matches:
        return
    conditions = []
    for idx, match in enumerate(matches, start=1):
        before = segment[: match.start()]
        banner = _nearest_banner(before)
        if len(matches) == 1:
            condition = DEFAULT_CONDITION
        else:
            condition = _condition_from_banner(banner) or f"{DEFAULT_CONDITION}_{idx}"
        conditions.append({"condition": condition, "xml": textwrap.dedent(match.group(0).strip())})
    conditions = _dedupe_conditions(conditions)

    contract = _contract_key(label)
    if contract in records:
        records[contract]["conditions"] = _dedupe_conditions(records[contract]["conditions"] + conditions)
        return

    request_element = _extract_request_element(conditions[0]["xml"])
    records[contract] = {
        "contract": contract,
        "module": _module_name(label),
        "label": label,
        "conditions": conditions,
        "request_element": request_element,
        "operation_mul_comment": _operation_mul_comment(request_element),
    }


def _split_label(label):
    match = _LABEL_SC_RE.match(label + ":")
    digits, version_letter, version_digits = match.group(1), match.group(2), match.group(3)
    return digits, version_letter, version_digits


def _contract_key(label):
    # handle different versions for a same service contract
    digits, version_letter, version_digits = _split_label(label)
    return f"SC{digits}{version_letter or ''}{version_digits or ''}"


def _module_name(label):
    # handle module name
    digits, version_letter, version_digits = _split_label(label)
    return f"sc{digits}{(version_letter or '').lower()}{version_digits or ''}"


def _nearest_banner(before):
    # handle comment
    for line in reversed(before.splitlines()):
        if line.strip().startswith("#"):
            return line
    return ""


def _condition_from_banner(banner):
    # handle multiple # defined in the file
    text = banner.strip("# ").strip()
    mul_comment = re.sub(r"\s+", "_", text).lower()
    mul_comment = re.sub(r"[^a-z0-9_]+", "_", mul_comment).strip("_")
    return mul_comment


def _dedupe_conditions(conditions):
    counts = {}
    result = []
    for item in conditions:
        name = item["condition"]
        counts[name] = counts.get(name, 0) + 1
        if counts[name] > 1:
            name = f"{name}_{counts[name]}"
        result.append({"condition": name, "xml": item["xml"]})
    return result


def _extract_request_element(raw_xml):
   # verify request body
    root = ET.fromstring(raw_xml)
    body = next((child for child in root if child.tag.rsplit("}", 1)[-1] == "Body"), None)
    if body is None:
        raise ValueError("No Body element found in payload")
    children = list(body)
    if not children:
        raise ValueError("Body is empty")
    return children[0].tag.rsplit("}", 1)[-1]


def _operation_mul_comment(request_element):
    # split request name
    base = re.sub(r"(?:Rqst|Request)$", "", request_element, flags=re.IGNORECASE)
    snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", base)
    return snake.lower()


def _rename_title(mul_comment):
    # rename title
    return mul_comment.replace("_", " ").title()


def build_payload_module(sc):
    # generate payload content
    if len(sc["conditions"]) == 1:
        return f'''{sc["contract"]}_PAYLOAD = """{sc["conditions"][0]["xml"]}"""


def get_payload_{sc["module"]}():
    return {sc["contract"]}_PAYLOAD


def get_headers_{sc["module"]}():
    return {{
        "Content-Type": "application/xml",
        "MSD-Sub-Env": "{MSD_SUB_ENV}",
    }}
'''
    entries = ",\n".join(f'    "{item["condition"]}": """{item["xml"]}"""' for item in sc["conditions"])
    default_condition = sc["conditions"][0]["condition"]
    return f'''{sc["contract"]}_PAYLOADS = {{
{entries}
}}


def get_payload_{sc["module"]}(condition="{default_condition}"):
    return {sc["contract"]}_PAYLOADS[condition]


def get_headers_{sc["module"]}():
    return {{
        "Content-Type": "application/xml",
        "MSD-Sub-Env": "{MSD_SUB_ENV}",
    }}
'''


def build_payload_setup(sc):
    # update payload_setup.py
    if len(sc["conditions"]) == 1:
        body = f"payloads.{sc['module']}.get_payload_{sc['module']}()"
    else:
        body = f"payloads.{sc['module']}.get_payload_{sc['module']}(condition=condition)"
    return f'''
def {sc["module"]}_payload_setup(condition="{sc["conditions"][0]["condition"]}"):
    return {{
        "request_body": {body},
        "header": payloads.{sc["module"]}.get_headers_{sc["module"]}(),
        "condition": condition,
    }}
'''


def build_feature(sc):
    # create feature files
    title = f"Comparison Testing - {sc['contract']} - {_rename_title(sc['operation_mul_comment'])}"
    tag = "@"
    width = max(len(item["condition"]) for item in sc["conditions"])
    header = f"      | {'condition':<{width}} |"
    rows = "\n".join(f"      | {item['condition']:<{width}} |" for item in sc["conditions"])
    return f"""{tag}comparison
Feature: {title}
  As a client,
  I want to send {sc["contract"]} {sc["operation_mul_comment"].replace("_", " ")} requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical

  {tag}positive
  Scenario Outline: Compare {sc["contract"]} successful responses between IIB and Azure
    Given I create the {sc["contract"]} api payload for <condition>
    When I send {sc["contract"]} request to IIB endpoint
    And I send {sc["contract"]} request to Azure endpoint
    Then I can see all the responses are identical for {sc["contract"]}

    Examples:
{header}
{rows}
"""


def build_steps_def(sc):
    # create python files in steps_def
    scenario_name = f"Compare {sc['contract']} successful responses between IIB and Azure"
    return f'''import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import {sc["module"]}_payload_setup
from utils.bdd_utils.scenario import scenario


@allure.testcase("{ALLURE_TESTCASE_URL}", "User Story")
@scenario("{scenario_name}")
def test_compare_{sc["module"]}_successful_responses():
    """{scenario_name}"""


@given(parsers.parse("I create the {sc["contract"]} api payload for {{condition}}"), target_fixture="payload")
def create_{sc["module"]}_payload(condition):
    return {sc["module"]}_payload_setup(condition=condition)


@when("I send {sc["contract"]} request to IIB endpoint", target_fixture="response_iib")
def send_{sc["module"]}_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("{sc["contract"]}", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send {sc["contract"]} request to Azure endpoint", target_fixture="response_azure")
def send_{sc["module"]}_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("{sc["contract"]}", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@then("I can see all the responses are identical for {sc["contract"]}")
def compare_{sc["module"]}_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "{sc["contract"]}", ignore_element_order=True)
'''


def _append_payload_setup(sc):
    # create payload files for every service contract
    text = PAYLOAD_SETUP_FILE.read_text(encoding="utf-8")
    if f"def {sc['module']}_payload_setup" in text:
        return
    with PAYLOAD_SETUP_FILE.open("a", encoding="utf-8") as fh:
        fh.write(build_payload_setup(sc))


def _register_modules_in_init(scs):
    # update the init file
    text = PAYLOAD_DATA_INIT.read_text(encoding="utf-8")
    missing = [sc["module"] for sc in scs if sc["module"] not in text]
    if not missing:
        return
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("from ..payload_data import ("):
            if not line.endswith(")"):
                raise RuntimeError("Unexpected payload_data import line in __init__.py (expected it to end with ')')")
            lines[i] = line[:-1] + ", " + ", ".join(missing) + ")"
            break
    else:
        raise RuntimeError("Could not find the payload_data import line in __init__.py")
    PAYLOAD_DATA_INIT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    xml_files = sorted(SCRIPTS_DIR.glob("*.xml"))
    if not xml_files:
        print("No *.xml payload files found in scripts/", file=sys.stderr)
        sys.exit(1)
    total_scs = 0
    for xml_file in xml_files:
        batch_match = _BATCH_FILE_RE.search(xml_file.stem)
        if not batch_match:
            print(
                f"SKIP {xml_file.name}: filename does not contain 'batch<N>' to derive the target directory",
                file=sys.stderr
            )
            continue
        batch_dir = COMPARISON_ROOT / f"batch_{batch_match.group(1)}"
        features_dir = batch_dir / "features"
        steps_dir = batch_dir / "steps_def"
        features_dir.mkdir(parents=True, exist_ok=True)
        steps_dir.mkdir(parents=True, exist_ok=True)

        scs = parse_payload_file(xml_file)
        for sc in scs:
            (PAYLOAD_DIR / f"{sc['module']}.py").write_text(build_payload_module(sc), encoding="utf-8")
            (features_dir / f"{sc['module']}_{sc['operation_mul_comment']}.feature").write_text(
                build_feature(sc), encoding="utf-8"
            )
            (steps_dir / f"{sc['module']}_{sc['operation_mul_comment']}_test.py").write_text(
                build_steps_def(sc), encoding="utf-8"
            )
            _append_payload_setup(sc)
        _register_modules_in_init(scs)

        for sc in scs:
            conditions = ", ".join(item["condition"] for item in sc["conditions"])
            print(
                f"generated {sc['contract']} ({xml_file.stem}): {sc['module']}.py, "
                f"{sc['module']}_{sc['operation_mul_comment']}.feature, "
                f"{sc['module']}_{sc['operation_mul_comment']}_test.py, {sc['module']}_payload_setup"
                f" [{conditions}]"
            )
        total_scs += len(scs)
        print(f"{xml_file.name}: {len(scs)} service contracts")
    print(f"Done: {total_scs} service contracts across {len(xml_files)} xml file(s)")


if __name__ == "__main__":
    main()
