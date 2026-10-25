import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp871_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP871 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3644", "API-3644")
@scenario("Compare DP871 successful transaction response")
def test_compare_dp871_successful_transaction_response():
    """Compare DP871 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP871 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3644", "API-3644")
@scenario("Compare DP871 unsuccessful transaction response")
def test_compare_dp871_unsuccessful_transaction_response():
    """Compare DP871 unsuccessful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the DP871 comparison payload for "{condition}"'), target_fixture="payload")
def create_dp871_comparison_payload(condition):
    return dp871_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the DP871 request to IIB endpoint", target_fixture="response_iib")
def send_dp871_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP871", system="IIB", sub_system="MYMSD")

    endpoint = f"{endpoint}?transactionId={payload['params']['transactionId']}"

    return api_client.send_rest_put_request(endpoint, payload["request_body"], payload["header"])


@when("I send the DP871 request to Azure endpoint", target_fixture="response_azure")
def send_dp871_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP871", system="AZURE")

    endpoint = f"{endpoint}?transactionId={payload['params']['transactionId']}"

    return api_client.send_rest_put_request(endpoint, payload["request_body"], payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP871")
def compare_all_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP871")
