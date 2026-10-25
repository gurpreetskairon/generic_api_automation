import json

import allure
import pytest
import requests
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.payload_setup import dp605_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check DP605 successful notify special caution response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3017", "User Story")
@scenario("Check DP605 successful notify special caution response")
def test_dp605_successful_notify_special_caution_response():
    """Check DP605 successful notify special caution response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check DP605 unsuccessful response for invalid client number
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3017", "User Story")
@scenario("Check DP605 unsuccessful response for invalid client number")
def test_dp605_unsuccessful_response_for_invalid_client_number():
    """Check DP605 unsuccessful response for invalid client number"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse(
        'I created the correct DP605 notify special caution payload for STAR with category "{category_code}" and type "{type_code}"'
    ),
    target_fixture="payload"
)
def create_correct_dp605_notify_special_caution_payload(category_code, type_code):
    return dp605_payload_setup(condition="valid_client", category_code=category_code, type_code=type_code)


@given("I used a valid client number as the DP605 path parameter", target_fixture="payload")
def use_valid_client_number_as_dp605_path_parameter(payload):
    return dp605_payload_setup(
        condition="valid_client", category_code=payload["category_code"], type_code=payload["type_code"]
    )


@given("I used an invalid client number as the DP605 path parameter")
def use_invalid_client_number_as_dp605_path_parameter(payload):
    invalid_payload = dp605_payload_setup(
        condition="invalid_client_number",
        category_code=payload["category_code"],
        type_code=payload["type_code"],
        system="AZURE"
    )

    payload.clear()
    payload.update(invalid_payload)

    assert payload["condition"] == "invalid_client_number"
    assert payload["client_number"] != ""
    assert payload["encoded_client_number"] in payload["endpoint_url"]

    return payload


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the DP605 notify special caution request to the Azure endpoint", target_fixture="response")
def send_dp605_notify_special_caution_request_to_azure(payload):
    endpoint = payload["endpoint_url"]
    headers = payload["header"].copy()
    request_body = payload["request_body"]

    safe_headers = headers.copy()
    if "Authorization" in safe_headers:
        safe_headers["Authorization"] = "***masked***"
    if "x-jws-signature" in safe_headers:
        safe_headers["x-jws-signature"] = "***masked***"

    allure.attach(endpoint, name="DP605 Azure endpoint", attachment_type=allure.attachment_type.TEXT)

    allure.attach(
        json.dumps(safe_headers, indent=2), name="DP605 request headers", attachment_type=allure.attachment_type.JSON
    )

    allure.attach(
        json.dumps(request_body, indent=2), name="DP605 request body", attachment_type=allure.attachment_type.JSON
    )
    response = requests.post(url=endpoint, headers=headers, json=request_body, verify=False)

    allure.attach(str(response.status_code), name="DP605 HTTP status code", attachment_type=allure.attachment_type.TEXT)

    allure.attach(response.text, name="DP605 response body", attachment_type=allure.attachment_type.TEXT)

    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse('I can see the "{expected_message}" response returned'))
def verify_dp605_response_message_returned(response, expected_message):
    actual_message = _get_dp605_service_result(response)["message"]

    assert actual_message == expected_message, (
        f"Expected message: {expected_message}. Actual message: {actual_message}. "
        f"HTTP status code: {response.status_code}. Response body: {response.text}"
    )


@then(parsers.parse("I can see HTTP status code {expected_status_code:d} returned"))
def verify_dp605_http_status_code(response, expected_status_code):
    actual_status_code = response.status_code

    assert actual_status_code == expected_status_code, (
        f"Expected HTTP status code: {expected_status_code}. " f"Actual HTTP status code: {actual_status_code}"
    )


@then(parsers.parse("I can see result code {expected_result_code} returned in the JSON response"))
def verify_dp605_result_code(response, expected_result_code):
    actual_result_code = _get_dp605_service_result(response)["code"]

    assert actual_result_code == expected_result_code, (
        f"Expected result code: {expected_result_code}. " f"Actual result code: {actual_result_code}"
    )


@then(parsers.parse('I can see result message "{expected_result_message}" returned in the JSON response'))
def verify_dp605_result_message(response, expected_result_message):
    actual_result_message = _get_dp605_service_result(response)["message"]

    assert actual_result_message == expected_result_message, (
        f"Expected result message: {expected_result_message}. " f"Actual result message: {actual_result_message}"
    )


def _get_dp605_service_result(response):
    try:
        response_body = response.json()
    except ValueError:
        raise AssertionError(f"DP605 response is not valid JSON. Response body: {response.text}")

    assert (
        "serviceResults" in response_body
    ), f"'serviceResults' is missing from DP605 response. Response body: {response_body}"

    assert response_body[
        "serviceResults"
    ], f"'serviceResults' is empty in DP605 response. Response body: {response_body}"

    return response_body["serviceResults"][0]
