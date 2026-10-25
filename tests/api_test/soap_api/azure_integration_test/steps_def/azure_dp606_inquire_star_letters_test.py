import allure
import pytest
from pytest_bdd import given, parsers, then

from apps.services.integration_soap.payload_data.dp606 import url_azure
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp606_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check whether the DP606 responses are the same across different endpoints
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3018", "User Story")
@scenario("Check whether the DP606 responses are the same across different endpoints")
def test_check_dp606_positive():
    """Check whether the DP606 responses are the same across different endpoints"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check responses are the same across different endpoints with different conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3018", "User Story")
@scenario("Check DP606 responses are the same across different endpoints with different conditions")
def test_check_dp606_different_conditions():
    """Check DP606 responses are the same across different endpoints with different conditions"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check DP606 responses with unsupported methods
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3018", "User Story")
@scenario("Check DP606 responses with unsupported methods")
def test_check_dp606_different_methods():
    """Check DP606 responses with unsupported methods"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct payload", target_fixture="payload")
def create_correct_payload():
    azure_payload = dp606_payload_setup(azure=True)
    return azure_payload


@given(parsers.parse("I create the payload with {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    azure_payload = dp606_payload_setup(conditions=conditions, azure=True)
    return azure_payload


@given("I send the request to the Azure DP606 endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP606", system="AZURE")
    return api_client.send_get_request(url_azure(endpoint, payload), headers=payload, raise_on_error=False, timeout=60)


@given(parsers.parse("I send the request to the Azure DP606 with {method}"), target_fixture="response_azure")
def send_azure_request_with_method(api_client, payload, method):
    endpoint = build_api_endpoint("DP606", system="AZURE")
    if method == "POST":
        return api_client.send_post_request(url_azure(endpoint, payload), payload={}, headers=payload)
    elif method == "PUT":
        return api_client.send_put_request(url_azure(endpoint, payload), payload={}, headers=payload)
    else:
        return api_client.send_get_request(url_azure(endpoint, payload), headers=payload)


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I see the response status code matches the expected code {status_code}"))
def validate_response_status_code(api_client, response_azure, status_code):
    api_client.compare_status_code(status_code, str(response_azure[1]))


# @then(parsers.parse("I see the response matches the {conditions} expected response and {status} on file"))
# def validate_response(api_client, response_azure, conditions, status):
#     api_client.compare_status_code(status, str(response_azure[1]))
#     error_400_conditions = ["invalid requestDateTime"]
#     error_500_conditions = [
#         "missing transactionId",
#         "invalid transactionId",
#         "missing sourceSystem",
#         "missing requestDateTime",
#         "missing client",
#         "missing auditID",
#         "invalid auditID",
#     ]
#     # error_405_conditions = ["post_method", "put_method"]
#     if conditions in error_400_conditions:
#         expected_response = json.dumps(responses.error_400)
#         api_client.compare_error_strings(expected_response, response_azure[0], "DP606", system="on file")
#     elif conditions in error_500_conditions:
#         expected_response = json.dumps(responses.error_500)
#         api_client.compare_error_strings(expected_response, response_azure[0], "DP606", system="on file")
#     elif conditions == "invalid client":
#         expected_response = json.dumps(responses.invalid_client)
#         api_client.compare_json_responses(expected_response, response_azure[2], "DP606", system="on file")
#     else:
#         expected_response = json.dumps(responses.positive_scenario)
#         api_client.compare_json_responses(expected_response, response_azure[0], "DP606", system="on file")
