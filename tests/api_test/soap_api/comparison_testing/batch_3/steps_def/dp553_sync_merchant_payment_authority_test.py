import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp553_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP553 successful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3987", "API-3987")
@scenario("Compare DP553 successful transaction responses")
def test_compare_dp553_successful_transaction_responses():
    """Compare DP553 successful transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP553 unsuccessful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3987", "API-3987")
@scenario("Compare DP553 unsuccessful transaction responses")
def test_compare_dp553_unsuccessful_transaction_responses():
    """Compare DP553 unsuccessful transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct DP553 api payload with different {conditions}"), target_fixture="payload")
def create_dp553_payload_with_condition(conditions):
    return dp553_payload_setup(conditions)


@given("I send the DP553 request to IIB endpoint", target_fixture="response_iib")
def send_dp553_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP553", system="IIB", sub_system="CMS")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the DP553 request to Azure endpoint", target_fixture="response_azure")
def send_dp553_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP553", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP553")
def compare_all_dp553_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "DP553")
