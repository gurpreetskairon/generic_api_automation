"""
<<<<<<< HEAD
generic_api_test.py
=======
test_generic_api_steps.py
>>>>>>> 6ac2d0d0 (added my generic api script code)

Generic, reusable step definitions for API testing with pytest-bdd.
Every CSV row (via the `test_case` fixture from conftest.py) drives one
run of this same scenario, so this file never needs to grow when new
endpoints/test cases are added -- only data/api_test_cases.csv does.
"""
<<<<<<< HEAD
import json
=======
>>>>>>> 6ac2d0d0 (added my generic api script code)
import os
import allure
import pytest
from pytest_bdd import scenario, given, when, then
from tests.generic.conftest import api_context, get_apim_base_url, get_iib_base_url, payload_factory
from utils.api.json_parser import query_json
from utils.comparison.payload_resolver import parse_validate_data, detect_response_type, resolve_query_params, \
    resolve_header_placeholders
from utils.comparison.response_comparator import compare_responses, compare_values, parse_ignore_fields
from utils.comparison.allure_reporting import classify_differences, build_side_by_side_html
from utils.api.xml_parser import query_xml
<<<<<<< HEAD
from utils.helpers.async_callback import write_callback_file
=======
>>>>>>> 6ac2d0d0 (added my generic api script code)


@scenario("./tests/generic/features/generic_api.feature", "Validate an API response against expected data")
def test_generic_api_request(testcase_row, api_context):
    pass


# --------------------------------------------------------------------------
# Given I fetch the endpoint
# --------------------------------------------------------------------------

@given("I fetch the endpoint")
def fetch_endpoint(testcase_row, metadata, api_context):
<<<<<<< HEAD
    print(testcase_row)
=======
>>>>>>> 6ac2d0d0 (added my generic api script code)
    sc_id = testcase_row["SERVICE_CONTRACT"]
    meta = metadata.get(sc_id)

    if meta is None:
        pytest.fail(f"No metadata found for Service Contract '{sc_id}' in metadata.csv")

<<<<<<< HEAD
    # set the contract_type from metadata
    if testcase_row["OVERRIDE_CONTRACT_TYPE"] == "":
        testcase_row["OVERRIDE_CONTRACT_TYPE"] = metadata.get("CONTRACT_TYPE", "")

=======
>>>>>>> 6ac2d0d0 (added my generic api script code)
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

<<<<<<< HEAD
    allure.attach(api_context.apim.base_url + api_context.apim.endpoint, name="APIM Endpoint", attachment_type=allure.attachment_type.TEXT)

=======
>>>>>>> 6ac2d0d0 (added my generic api script code)
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
<<<<<<< HEAD
        allure.attach(api_context.iib.base_url + api_context.iib.endpoint, name="IIB Endpoint", attachment_type=allure.attachment_type.TEXT)
=======

>>>>>>> 6ac2d0d0 (added my generic api script code)


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
<<<<<<< HEAD
        allure.attach(json.dumps(api_context.apim.query_params), name="APIM Query Params", attachment_type=allure.attachment_type.JSON)
=======
>>>>>>> 6ac2d0d0 (added my generic api script code)

        if api_context.is_comparison:
            iib_query_params = testcase_row.get("OVERRIDE_QUERY_STRING_FOR_IIB").strip()
            iib_query_params_placeholders = testcase_row.get("OVERRIDE_QUERY_STRING_PLACEHOLDER_VALUES_FOR_IIB").strip()
            if iib_query_params or iib_query_params_placeholders:
                if not iib_query_params:
                    iib_query_params = query_string
                query_params = resolve_query_params(iib_query_params, iib_query_params_placeholders)
            api_context.iib.query_params = query_params
<<<<<<< HEAD
            allure.attach(json.dumps(api_context.iib.query_params), name="IIB Query Params",
                          attachment_type=allure.attachment_type.JSON)

    ### HANDLE PAYLOADS
    payload, apim_fmt = payload_factory(testcase_row.get("PAYLOAD").strip(), testcase_row.get("PAYLOAD_PLACEHOLDER_VALUES").strip())
    if apim_fmt == "xml":
        allure_attachment_type = allure.attachment_type.XML
    elif apim_fmt == "json":
        allure_attachment_type = allure.attachment_type.JSON
    else:
        allure_attachment_type = allure.attachment_type.TEXT

    if payload:
        api_context.apim.request_body = payload
        allure.attach(api_context.apim.request_body, name="APIM Payload", attachment_type=allure_attachment_type)
=======

    ### HANDLE PAYLOADS
    payload = payload_factory(testcase_row.get("PAYLOAD").strip(), testcase_row.get("PAYLOAD_PLACEHOLDER_VALUES").strip())

    if payload:
        api_context.apim.request_body = payload
>>>>>>> 6ac2d0d0 (added my generic api script code)
        if api_context.is_comparison:
            iib_payload = testcase_row.get("OVERRIDE_PAYLOAD_FOR_IIB").strip()
            iib_payload_placeholders =  testcase_row.get("OVERRIDE_PAYLOAD_PLACEHOLDER_VALUES_FOR_IIB").strip()
            if iib_payload or iib_payload_placeholders:
                if not iib_payload:
                    iib_payload = testcase_row.get("PAYLOAD").strip()
<<<<<<< HEAD
                payload, iib_fmt = payload_factory(iib_payload, iib_payload_placeholders)

            api_context.iib.request_body = payload
            allure.attach(api_context.iib.request_body, name="IIB Payload", attachment_type=allure_attachment_type)

=======
                payload = payload_factory(iib_payload, iib_payload_placeholders)

            api_context.iib.request_body = payload
>>>>>>> 6ac2d0d0 (added my generic api script code)


# --------------------------------------------------------------------------
# When I send the request
# --------------------------------------------------------------------------
@when("I send the request")
<<<<<<< HEAD
def send_request(testcase_row, api_context):
    allure.attach(api_context.apim.method, name="HTTP Method", attachment_type=allure.attachment_type.TEXT)
=======
def send_request(api_context):
>>>>>>> 6ac2d0d0 (added my generic api script code)
    api_context.apim.send_request()
    if api_context.is_comparison:
        api_context.iib.send_request()

<<<<<<< HEAD
    contract_type = (testcase_row.get("OVERRIDE_CONTRACT_TYPE") or "").strip().lower()
    if contract_type == "async":
        callback_path = write_callback_file(testcase_row, api_context)
        allure.attach(str(callback_path), name="Callback File", attachment_type=allure.attachment_type.TEXT)

=======
>>>>>>> 6ac2d0d0 (added my generic api script code)

# --------------------------------------------------------------------------
# Then I should receive the expected status code
# --------------------------------------------------------------------------
@then("I should receive the expected status code")
def validate_status_code(testcase_row, api_context):
<<<<<<< HEAD
    # api_context.apim.print()
    allure.attach(str(api_context.apim.response.status), name="APIM Response Code",
                  attachment_type=allure.attachment_type.TEXT)
    if api_context.is_comparison:
        allure.attach(str(api_context.iib.response.status), name="IIB Response Code",
                      attachment_type=allure.attachment_type.TEXT)
=======
    api_context.apim.print()
    print("IIB")
>>>>>>> 6ac2d0d0 (added my generic api script code)
    # api_context.iib.print()
    if testcase_row["RESPONSE_CODE"]:
        api_context.apim.verify_response_status(testcase_row["RESPONSE_CODE"])


# --------------------------------------------------------------------------
# And I validate the testcase_row data
# --------------------------------------------------------------------------
@then("I validate the response data")
def validate_response_data(testcase_row, api_context):
    ignore_fields = parse_ignore_fields(testcase_row.get("COMPARISON_TO_IGNORE"))

<<<<<<< HEAD
    response_type = detect_response_type(api_context.apim.response)
    if response_type == "xml":
        allure_attachment_type = allure.attachment_type.XML
    elif response_type == "json":
        allure_attachment_type = allure.attachment_type.JSON
    else:
        allure_attachment_type = allure.attachment_type.TEXT

    apim_text = api_context.apim.response.text()
    allure.attach(apim_text, name="APIM Response", attachment_type=allure_attachment_type)
    print(f"allure_attachment_type: {allure_attachment_type}")

    print(f"APIM Response: {apim_text}")

    if api_context.is_comparison:
        iib_text = api_context.iib.response.text()
        print(f"IIB Response: {iib_text}")
        allure.attach(iib_text, name="IIB Response", attachment_type=allure_attachment_type)
=======
    if api_context.is_comparison:
        apim_text = api_context.apim.response.text()
        iib_text = api_context.iib.response.text()
>>>>>>> 6ac2d0d0 (added my generic api script code)

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
<<<<<<< HEAD
                attachment_type=allure_attachment_type,
=======
                attachment_type=allure.attachment_type.TEXT,
>>>>>>> 6ac2d0d0 (added my generic api script code)
            )
            allure.attach(
                build_side_by_side_html(iib_text, apim_text),
                name="IIB vs APIM Response Comparison",
                attachment_type=allure.attachment_type.HTML,
            )

        assert not report.has_differences(), report.to_text()
        return

    validate_dict = parse_validate_data(testcase_row["VALIDATE_DATA"])
<<<<<<< HEAD

=======
    response_type = detect_response_type(api_context.apim.response)
>>>>>>> 6ac2d0d0 (added my generic api script code)

    for key, expected_value in validate_dict.items():
        if response_type == "xml":
            actual_value = query_xml(api_context.apim.response.text(), key)
        elif response_type == "json":
            actual_value = query_json(api_context.apim.response.json(), key)
        else:
            raise ValueError(f"Unsupported response type: {response_type}")

        report = compare_values(actual_value, expected_value, label_a="Actual", label_b="Expected")
        assert not report.has_differences(), f"Mismatch for key '{key}':\n{report.to_text()}"
