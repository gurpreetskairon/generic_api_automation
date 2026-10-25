import allure
from pytest_bdd import given, parsers, then, when
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp833_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP833 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4136", "User Story")
@scenario("Compare DP833 successful responses between IIB and Azure")
def test_compare_dp833_successful_responses():
    """Compare DP833 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP833 api payload for {condition}"), target_fixture="payload")
def create_dp833_payload(condition):
    return dp833_payload_setup(condition=condition)


@when("I send DP833 request to IIB endpoint", target_fixture="response_iib")
def send_dp833_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP833", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, params=payload[1], headers=payload[0])


@when("I send DP833 request to Azure endpoint", target_fixture="response_azure")
def send_dp833_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP833", system="AZURE")
    return api_client.send_get_request(endpoint, params=payload[1], headers=payload[0])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP833")
def compare_dp833_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP833")
