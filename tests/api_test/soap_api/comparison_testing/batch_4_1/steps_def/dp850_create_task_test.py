import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp850_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP850 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3953", "API-3953")
@scenario("Compare DP850 successful transaction response")
def test_compare_dp850_successful_transaction_response():
    """Compare DP850 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct DP850 api payload with different {conditions}"), target_fixture="payload")
def create_dp850_payload_with_condition(conditions):
    return dp850_payload_setup(conditions)


@given("I send the DP850 request to IIB endpoint", target_fixture="response_iib")
def send_dp850_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP850", system="IIB", sub_system="MYMSD")

    return api_client.send_post_request(
        endpoint,
        payload=payload["request_body"],
        headers=payload["header"],
        params=payload["params"],
        json_payload=True
    )


@given("I send the DP850 request to Azure endpoint", target_fixture="response_azure")
def send_dp850_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP850", system="AZURE")

    return api_client.send_post_request(
        endpoint,
        payload=payload["request_body"],
        headers=payload["header"],
        params=payload["params"],
        json_payload=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP850")
def compare_all_dp850_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP850")
