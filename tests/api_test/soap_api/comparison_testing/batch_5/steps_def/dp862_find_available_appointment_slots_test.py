import allure
from pytest_bdd import given, parsers, then, when
from apps.services.integration_soap.payload_data.dp862 import update_dp862_endpoint
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp862_payload_setup
from utils.bdd_utils.scenario import scenario
from apps.services.integration_soap.soap_helpers import get_base64_encoded_string


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP862 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4130", "User Story")
@scenario("Compare DP862 successful responses between IIB and Azure")
def test_compare_dp862_successful_responses():
    """Compare DP862 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP862 negative response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4130", "User Story")
@scenario("Compare DP862 negative response between IIB and Azure")
def test_compare_dp862_negative_responses():
    """Compare DP862 negative response between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP862 api payload for {condition}"), target_fixture="payload")
def create_dp862_payload(condition):
    return dp862_payload_setup(condition=condition), condition


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP862 request to IIB endpoint", target_fixture="response_iib")
def send_dp862_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP862", system="IIB", sub_system="MYMSD")
    endpoint = update_dp862_endpoint(endpoint, payload[1])
    return api_client.send_get_request(endpoint, params=payload[0][1], headers=payload[0][0], raise_on_error=False)


@when("I send DP862 request to Azure endpoint", target_fixture="response_azure")
def send_dp862_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP862", system="AZURE")
    endpoint = update_dp862_endpoint(endpoint, payload[1])
    payload[0][0]['Authorization'] = f"Basic {get_base64_encoded_string("mymsduser:password")}"
    return api_client.send_get_request(endpoint, params=payload[0][1], headers=payload[0][0], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP862")
def compare_dp862_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP862")
