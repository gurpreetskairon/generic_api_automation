import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp811_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP811 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3646", "API-3646")
@scenario("Compare DP811 successful transaction response")
def test_compare_dp811_successful_transaction_response():
    """Compare DP811 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP811 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3646", "API-3646")
@scenario("Compare DP811 unsuccessful transaction response")
def test_compare_dp811_unsuccessful_transaction_response():
    """Compare DP811 unsuccessful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the DP811 comparison request for "{condition}"'), target_fixture="payload")
def create_dp811_comparison_request(condition):
    return dp811_payload_setup(condition)


@given("I send the DP811 request to IIB endpoint", target_fixture="response_iib")
def send_dp811_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP811", system="IIB", sub_system="MYMSD")

    return api_client.send_get_request(endpoint, headers=payload["header"], params=payload["params"])


@given("I send the DP811 request to Azure endpoint", target_fixture="response_azure")
def send_dp811_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP811", system="AZURE")

    return api_client.send_get_request(endpoint, headers=payload["header"], params=payload["params"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP811")
def compare_all_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(
        response_iib[0], response_azure[0], "DP811", ignore_array_order=True, ignore_numeric_strings=True
    )
