from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp247_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP247 successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3645", "User Story")
@scenario("Compare DP247 successful responses")
def test_compare_DP247_successful_response():
    """Compare DP247 successful responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP247 responses for no matching clients
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3645", "User Story")
@scenario("Compare DP247 responses for no matching clients")
def test_compare_DP247_response_for_no_matching_clients():
    """Compare DP247 responses for no matching clients"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare DP247 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3645", "User Story")
@scenario("Compare DP247 responses with invalid data")
def test_compare_DP247_response_with_invalid_data():
    """Compare DP247 responses with invalid data"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare DP247 responses with an invalid client number
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3645", "User Story")
@scenario("Compare DP247 responses with an invalid client number")
def test_compare_DP247_response_with_invalid_client_number():
    """Compare DP247 responses with an invalid client number"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return dp247_payload_setup()


@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return dp247_payload_setup(conditions=conditions)


@given("I send the request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = f"{build_api_endpoint('DP247', system='IIB', sub_system='MYMSD')}?{payload[2]}"
    return api_client.send_post_request(
        endpoint, payload=payload[0], headers=payload[1], json_payload=True, raise_error=False
    )


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = f"{build_api_endpoint('DP247', system='AZURE')}?{payload[2]}"
    return api_client.send_post_request(
        endpoint, payload=payload[0], headers=payload[1], json_payload=True, raise_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP247")
