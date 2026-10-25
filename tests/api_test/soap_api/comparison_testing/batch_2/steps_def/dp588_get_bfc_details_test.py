import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp588_payload_setup
from utils.bdd_utils.scenario import scenario


@pytest.mark.skip(reason="DP588 is replaced by SC588")
# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP588 successful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3959", "API-3959")
@scenario("Compare DP588 successful transaction responses")
def test_compare_dp588_successful_transaction_responses():
    """Compare DP588 successful transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct DP588 api payload with different {conditions}"), target_fixture="payload")
def create_dp588_payload_with_condition(conditions):
    return dp588_payload_setup(conditions)


@given("I send the DP588 request to IIB endpoint", target_fixture="response_iib")
def send_dp588_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP588", system="IIB", sub_system="MYMSD")

    return api_client.send_get_request(url=endpoint, headers=payload["header"], params=payload["params"])


@given("I send the DP588 request to Azure endpoint", target_fixture="response_azure")
def send_dp588_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP588", system="AZURE")

    return api_client.send_get_request(url=endpoint, headers=payload["header"], params=payload["params"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP588")
def compare_all_dp588_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP588")
