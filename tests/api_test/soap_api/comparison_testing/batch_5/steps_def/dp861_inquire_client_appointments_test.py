import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp861_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP861 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4138", "User Story")
@scenario("Compare DP861 successful responses between IIB and Azure")
def test_compare_dp861_successful_responses():
    """Compare DP861 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP861 successful responses between IIB and Azure with an invalid swn
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4138", "User Story")
@scenario("Compare DP861 successful responses between IIB and Azure with an invalid swn")
def test_compare_dp861_successful_responses_with_invalid_swn():
    """Compare DP861 successful responses between IIB and Azure with an invalid swn"""


@given(parsers.parse("I create the DP861 api payload for {condition}"), target_fixture="payload")
def create_dp861_payload(condition):
    return dp861_payload_setup(condition=condition)


@when("I send DP861 request to IIB endpoint", target_fixture="response_iib")
def send_dp861_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP861", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, params=payload[1], headers=payload[0])


@when("I send DP861 request to Azure endpoint", target_fixture="response_azure")
def send_dp861_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP861", system="AZURE")
    return api_client.send_get_request(endpoint, params=payload[1], headers=payload[0])


@then("I can see all the responses are identical for DP861")
def compare_dp861_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP861", exclude_fields=["requestDateTime"])
