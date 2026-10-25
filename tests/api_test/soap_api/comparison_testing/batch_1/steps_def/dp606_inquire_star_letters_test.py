import allure
from pytest_bdd import given, parsers, then

from apps.services.integration_soap.payload_data.dp606 import url_azure, url_iib
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


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check responses across different endpoints with different conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3018", "User Story")
@scenario("Check DP606 responses are the same across different endpoints with different conditions")
def test_check_dp606_different_conditions():
    """Check DP606 responses are the same across different endpoints with different conditions"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    iib_payload = dp606_payload_setup()
    azure_payload = dp606_payload_setup(azure=True)
    payloads = {"iib_headers": iib_payload, "azure_headers": azure_payload}
    return payloads


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    iib_payload = dp606_payload_setup(conditions=conditions)
    azure_payload = dp606_payload_setup(conditions=conditions, azure=True)
    payloads = {"iib_headers": iib_payload, "azure_headers": azure_payload, "conditions": conditions}

    return payloads


@given("I send inquire participant request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP606", system="IIB")
    return api_client.send_get_request(
        url_iib(endpoint, payload), headers=payload["iib_headers"], raise_on_error=False, timeout=60
    )


@given("I send the inquire participant request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP606", system="AZURE")
    return api_client.send_get_request(
        url_azure(endpoint, payload), headers=payload["azure_headers"], raise_on_error=False, timeout=60
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I can see the responses are identical for {response_type}"))
def validate_response(api_client, response_iib, response_azure, response_type):
    if response_type == "error string":
        api_client.compare_error_strings(response_iib[0], response_azure[0], "DP606")
    else:
        api_client.compare_json_responses(response_iib[0], response_azure[0], "DP606")
