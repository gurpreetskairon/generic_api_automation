import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp879_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP879 successful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4259", "User Story")
@scenario("Compare DP879 successful responses between DataPower and Azure")
def test_compare_dp879_successful_responses():
    """Compare DP879 successful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP879 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4259", "User Story")
@scenario("Compare DP879 unsuccessful responses between DataPower and Azure")
def test_compare_dp879_unsuccessful_responses():
    """Compare DP879 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP879 api request for {condition}"), target_fixture="payload")
def create_dp879_payload(condition):
    return dp879_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP879 request to DataPower endpoint", target_fixture="response_iib")
def send_dp879_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP879", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


@when("I send DP879 request to Azure endpoint", target_fixture="response_azure")
def send_dp879_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP879", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP879")
def validate_dp879_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "dp879", ignore_array_order=True)
