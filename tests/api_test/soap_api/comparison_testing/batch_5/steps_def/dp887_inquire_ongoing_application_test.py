import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp887_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP887 successful response between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4247", "User Story")
@scenario("Compare DP887 successful response between DataPower and Azure")
def test_compare_dp887_successful_response():
    """Compare DP887 successful response between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP887 successful sub-result responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4247", "User Story")
@scenario("Compare DP887 successful sub-result responses between DataPower and Azure")
def test_compare_dp887_successful_sub_result_responses():
    """Compare DP887 successful sub-result responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare DP887 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4247", "User Story")
@scenario("Compare DP887 unsuccessful responses between DataPower and Azure")
def test_compare_dp887_unsuccessful_responses():
    """Compare DP887 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP887 api request for {condition}"), target_fixture="payload")
def create_dp887_payload(condition):
    return dp887_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP887 request to DataPower endpoint", target_fixture="response_iib")
def send_dp887_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP887", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


@when("I send DP887 request to Azure endpoint", target_fixture="response_azure")
def send_dp887_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP887", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP887")
def validate_dp887_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "dp887", ignore_array_order=True)
