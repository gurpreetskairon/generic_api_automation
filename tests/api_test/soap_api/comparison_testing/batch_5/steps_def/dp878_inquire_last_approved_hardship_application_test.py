import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp878_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP878 successful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3905", "User Story")
@scenario("Compare DP878 successful responses between DataPower and Azure")
def test_compare_dp878_successful_responses():
    """Compare DP878 successful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP878 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3905", "User Story")
@scenario("Compare DP878 unsuccessful responses between DataPower and Azure")
def test_compare_dp878_unsuccessful_responses():
    """Compare DP878 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP878 api request for {condition}"), target_fixture="payload")
def create_dp878_payload(condition):
    return dp878_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP878 request to DataPower endpoint", target_fixture="response_iib")
def send_dp878_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP878", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


@when("I send DP878 request to Azure endpoint", target_fixture="response_azure")
def send_dp878_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP878", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP878")
def validate_dp878_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "dp878", ignore_array_order=True)
