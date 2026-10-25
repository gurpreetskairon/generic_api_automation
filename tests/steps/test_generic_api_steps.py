"""
test_generic_api_steps.py

Generic, reusable step definitions for API testing with pytest-bdd.
Every CSV row (via the `test_case` fixture from conftest.py) drives one
run of this same scenario, so this file never needs to grow when new
endpoints/test cases are added -- only data/api_test_cases.csv does.
"""
import os
import allure
import pytest
from pytest_bdd import scenario, given, when, then
from tests.conftest import api_context, get_apim_base_url, get_iib_base_url, payload_factory
from utils.api.json_parser import query_json
from utils.comparison.payload_resolver import parse_validate_data, detect_response_type, resolve_query_params, \
    resolve_header_placeholders
from utils.comparison.response_comparator import compare_responses, compare_values, parse_ignore_fields
from utils.comparison.allure_reporting import classify_differences, build_side_by_side_html
from utils.api.xml_parser import query_xml


@scenario("../features/generic_api.feature", "Validate an API response against expected data")
def test_generic_api_request(testcase_row, api_context):
    pass


# --------------------------------------------------------------------------
# Given I fetch the endpoint
# --------------------------------------------------------------------------

@given("I fetch the endpoint")
def fetch_endpoint(testcase_row, metadata, api_context):
    sc_id = testcase_row["SERVICE_CONTRACT"]
    meta = metadata.get(sc_id)

    if meta is None:
        pytest.fail(f"No metadata found for Service Contract '{sc_id}' in metadata.csv")

    if testcase_row.get("OVERRIDE_PATH"):
        endpoint = testcase_row["OVERRIDE_PATH"].strip()
    else:
        endpoint = meta["PATH"]

    # get headers
    raw_header = os.getenv(meta["HEADER"])

    header_placeholder_values = parse_validate_data(
        testcase_row.get("HEADER_PLACEHOLDER_VALUES", "").strip()
    )
    raw_header = resolve_header_placeholders(raw_header, header_placeholder_values)

    # get http method
    if testcase_row.get("OVERRIDE_HTTP_METHOD"):
        http_method = testcase_row["OVERRIDE_HTTP_METHOD"].strip()
    else:
        http_method = meta.get("HTTP_METHOD", "POST")   # default value is post

    # APIM BASE URL
    if meta.get("OVERRIDE_APIM_BASE_URL"):
        api_context.apim.base_url = meta["OVERRIDE_APIM_BASE_URL"].strip()
    else:
        api_context.apim.base_url = get_apim_base_url()
    api_context.apim.endpoint = endpoint

    api_context.apim.headers = raw_header
    api_context.apim.method = http_method

    # ENDPOINT
    # IIB BASE URL
    if api_context.is_comparison:
        if meta.get("OVERRIDE_IIB_BASE_URL"):
            api_context.iib.base_url = meta["OVERRIDE_IIB_BASE_URL"].strip()
        else:
            api_context.iib.base_url = get_iib_base_url()
        api_context.iib.endpoint = endpoint
        api_context.iib.headers = raw_header
        api_context.iib.method = http_method



# --------------------------------------------------------------------------
# And the request information
# --------------------------------------------------------------------------
@given("the request information")
def request_information(testcase_row, api_context, payload_factory):
    query_string = testcase_row.get("QUERY_STRING", "").strip()
    if query_string:
        query_placeholder_values = parse_validate_data(
            testcase_row.get("QUERY_STRING_PLACEHOLDER_VALUES", "").strip()
        )
        query_params = resolve_query_params(query_string, query_placeholder_values)

        api_context.apim.query_params = query_params

        if api_context.is_comparison:
            iib_query_params = testcase_row.get("OVERRIDE_QUERY_STRING_FOR_IIB").strip()
            iib_query_params_placeholders = testcase_row.get("OVERRIDE_QUERY_STRING_PLACEHOLDER_VALUES_FOR_IIB").strip()
            if iib_query_params or iib_query_params_placeholders:
                if not iib_query_params:
                    iib_query_params = query_string
                query_params = resolve_query_params(iib_query_params, iib_query_params_placeholders)
            api_context.iib.query_params = query_params

    ### HANDLE PAYLOADS
    payload = payload_factory(testcase_row.get("PAYLOAD").strip(), testcase_row.get("PAYLOAD_PLACEHOLDER_VALUES").strip())

    if payload:
        api_context.apim.request_body = payload
        if api_context.is_comparison:
            iib_payload = testcase_row.get("OVERRIDE_PAYLOAD_FOR_IIB").strip()
            iib_payload_placeholders =  testcase_row.get("OVERRIDE_PAYLOAD_PLACEHOLDER_VALUES_FOR_IIB").strip()
            if iib_payload or iib_payload_placeholders:
                if not iib_payload:
                    iib_payload = testcase_row.get("PAYLOAD").strip()
                payload = payload_factory(iib_payload, iib_payload_placeholders)

            api_context.iib.request_body = payload


# --------------------------------------------------------------------------
# When I send the request
# --------------------------------------------------------------------------
@when("I send the request")
def send_request(api_context):
    api_context.apim.send_request()
    if api_context.is_comparison:
        api_context.iib.send_request()


# --------------------------------------------------------------------------
# Then I should receive the expected status code
# --------------------------------------------------------------------------
@then("I should receive the expected status code")
def validate_status_code(testcase_row, api_context):
    api_context.apim.print()
    print("IIB")
    # api_context.iib.print()
    if testcase_row["RESPONSE_CODE"]:
        api_context.apim.verify_response_status(testcase_row["RESPONSE_CODE"])


# --------------------------------------------------------------------------
# And I validate the testcase_row data
# --------------------------------------------------------------------------
@then("I validate the response data")
def validate_response_data(testcase_row, api_context):
    ignore_fields = parse_ignore_fields(testcase_row.get("COMPARISON_TO_IGNORE"))

    if api_context.is_comparison:
        apim_text = api_context.apim.response.text()
        iib_text = api_context.iib.response.text()

        report = compare_responses(
            apim_text,
            iib_text,
            label_a="APIM",
            label_b="IIB",
            ignore_fields=ignore_fields,
        )

        if report.has_differences():
            allure.attach(
                classify_differences(report.to_text()),
                name="Failure Classification",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                build_side_by_side_html(iib_text, apim_text),
                name="IIB vs APIM Response Comparison",
                attachment_type=allure.attachment_type.HTML,
            )

        assert not report.has_differences(), report.to_text()
        return

    validate_dict = parse_validate_data(testcase_row["VALIDATE_DATA"])
    response_type = detect_response_type(api_context.apim.response)

    for key, expected_value in validate_dict.items():
        if response_type == "xml":
            actual_value = query_xml(api_context.apim.response.text(), key)
        elif response_type == "json":
            actual_value = query_json(api_context.apim.response.json(), key)
        else:
            raise ValueError(f"Unsupported response type: {response_type}")

        report = compare_values(actual_value, expected_value, label_a="Actual", label_b="Expected")
        assert not report.has_differences(), f"Mismatch for key '{key}':\n{report.to_text()}"
