"""
async_validation_test.py

Step definitions for validating async contract responses. Every row in
data/async_validations.csv (via the `async_case` fixture in conftest.py)
drives one run of this same scenario.
"""
import json
import os

import allure
import pytest
from pytest_bdd import scenario, given, when, then

from utils.api.json_parser import query_json
from utils.api.xml_parser import query_xml
from tools.async_validation.base import ResponseNotFound
from utils.comparison.allure_reporting import classify_differences, build_side_by_side_html
from utils.comparison.payload_resolver import parse_validate_data
from utils.comparison.response_comparator import compare_responses, compare_values, parse_ignore_fields


@scenario("./tests/async_validation/features/async_validation.feature",
          "Validate an async response against expected data")
def test_async_validation(async_case):
    pass


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def _is_comparison(callback_data) -> bool:
    # TEST_TYPE was recorded when the callback file was written. A file created
    # by an integration run has no IIB response in Splunk to compare against.
    return (callback_data.get("TEST_TYPE") or "comparison").strip().lower() == "comparison"


def _detect_type(text: str) -> str:
    stripped = (text or "").lstrip()
    if stripped.startswith("<"):
        return "xml"
    try:
        json.loads(stripped)
        return "json"
    except ValueError:
        return "text"


def _allure_type(kind: str):
    return {
        "xml": allure.attachment_type.XML,
        "json": allure.attachment_type.JSON,
    }.get(kind, allure.attachment_type.TEXT)


# --------------------------------------------------------------------------
# Given the callback file is loaded
# --------------------------------------------------------------------------
@given("the callback file is loaded")
def load_callback(async_case, callback_data):
    allure.attach(str(async_case["json_path"]), name="Callback File",
                  attachment_type=allure.attachment_type.TEXT)

    # Only a summary: the full file holds request bodies/headers we don't want in reports
    summary_keys = ("TEST_ID", "SERVICE_CONTRACT", "CONDITION", "TEST_TYPE",
                    "APIM_UUID", "IIB_UUID", "ASYNC_COMPARISON_TO_IGNORE",
                    "ASYNC_RESPONSE_CODE", "ASYNC_VALIDATE_DATA")
    summary = {k: callback_data.get(k) for k in summary_keys}
    allure.attach(json.dumps(summary, indent=2), name="Callback Summary",
                  attachment_type=allure.attachment_type.JSON)


# --------------------------------------------------------------------------
# When I retrieve the async responses
# --------------------------------------------------------------------------
@when("I retrieve the async responses")
def retrieve_responses(request, callback_data, async_result):
    apim_id = (callback_data.get("APIM_UUID") or "").strip()
    if not apim_id:
        pytest.fail("APIM_UUID is missing in the callback file")

    comparison = _is_comparison(callback_data)
    iib_id = (callback_data.get("IIB_UUID") or "").strip() or apim_id

    try:
        # Fixtures are requested here (not in the signature) so an
        # integration-only run never starts the Splunk browser.
        appinsights = request.getfixturevalue("appinsights_client")
        allure.attach(apim_id, name="APIM Transaction ID", attachment_type=allure.attachment_type.TEXT)
        async_result["apim"] = appinsights.get_response(apim_id)
        apim_kind = _detect_type(async_result["apim"].body)
        allure.attach(async_result["apim"].body, name="APIM Response", attachment_type=_allure_type(apim_kind))

        if comparison:
            splunk = request.getfixturevalue("splunk_client")
            allure.attach(iib_id, name="IIB Transaction ID", attachment_type=allure.attachment_type.TEXT)
            async_result["iib"] = splunk.get_response(iib_id)
            iib_kind = _detect_type(async_result["iib"].body)
            allure.attach(async_result["iib"].body, name="IIB Response", attachment_type=_allure_type(iib_kind))
    except ResponseNotFound as exc:
        pytest.fail(f"Async response not found (not arrived yet, or outside the search window): {exc}")


# --------------------------------------------------------------------------
# Then I should receive the expected response code
# --------------------------------------------------------------------------
@then("I should receive the expected response code")
def validate_response_code(callback_data, async_result):
    apim = async_result["apim"]
    allure.attach(str(apim.status_code), name="APIM Response Code", attachment_type=allure.attachment_type.TEXT)
    if "iib" in async_result:
        allure.attach(str(async_result["iib"].status_code), name="IIB Response Code",
                      attachment_type=allure.attachment_type.TEXT)

    expected = str(callback_data.get("ASYNC_RESPONSE_CODE") or "").strip()
    if not expected:
        return

    assert apim.status_code is not None, (
        f"ASYNC_RESPONSE_CODE is '{expected}' but no status code was found in the APIM log entry"
    )
    assert str(apim.status_code) == expected, (
        f"APIM response code mismatch: expected {expected}, got {apim.status_code}"
    )


# --------------------------------------------------------------------------
# And I validate the async response data
# --------------------------------------------------------------------------
@then("I validate the async response data")
def validate_response_data(callback_data, async_result):
    apim_text = async_result["apim"].body

    if "iib" in async_result:
        iib_text = async_result["iib"].body
        ignore_fields = parse_ignore_fields(callback_data.get("ASYNC_COMPARISON_TO_IGNORE"))

        report = compare_responses(
            apim_text,
            iib_text,
            label_a="APIM",
            label_b="IIB",
            ignore_fields=ignore_fields,
        )

        if report.has_differences():
            kind = _detect_type(apim_text)
            allure.attach(
                classify_differences(report.to_text()),
                name="Failure Classification",
                attachment_type=_allure_type(kind),
            )
            allure.attach(
                build_side_by_side_html(iib_text, apim_text),
                name="IIB vs APIM Response Comparison",
                attachment_type=allure.attachment_type.HTML,
            )

        assert not report.has_differences(), report.to_text()
        return

    raw_validate = (callback_data.get("ASYNC_VALIDATE_DATA") or "").strip()
    if not raw_validate:
        pytest.fail("ASYNC_VALIDATE_DATA is empty: nothing to validate for an integration run")

    validate_dict = parse_validate_data(raw_validate)
    kind = _detect_type(apim_text)

    for key, expected_value in validate_dict.items():
        if kind == "xml":
            actual_value = query_xml(apim_text, key)
        elif kind == "json":
            actual_value = query_json(json.loads(apim_text), key)
        else:
            raise ValueError(f"Unsupported response type: {kind}")

        report = compare_values(actual_value, expected_value, label_a="Actual", label_b="Expected")
        assert not report.has_differences(), f"Mismatch for key '{key}':\n{report.to_text()}"


# --------------------------------------------------------------------------
# And the callback file is cleaned up
# --------------------------------------------------------------------------
@then("the callback file is cleaned up")
def cleanup_callback_file(async_case):
    # Only reached when every earlier step passed, so failed validations keep their file.
    if os.getenv("ASYNC_KEEP_CALLBACKS", "false").strip().lower() == "true":
        return
    path = async_case["json_path"]
    path.unlink(missing_ok=True)
    allure.attach(f"Deleted {path}", name="Callback Cleanup", attachment_type=allure.attachment_type.TEXT)
