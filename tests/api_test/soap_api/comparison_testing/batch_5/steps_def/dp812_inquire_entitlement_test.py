from types import SimpleNamespace
import allure
from pytest_bdd import given, parsers, then
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp812_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP812 successful responses with different entitlement factors
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3911", "User Story")
@scenario("Compare DP812 successful responses with different entitlement factors")
def test_compare_dp812_successful_response_with_different_entitlement_factors():
    """Compare DP812 successful responses with different entitlement factors"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP812 successful responses with different entitlement factors
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3911", "User Story")
@scenario("Compare DP812 successful responses with different optional params")
def test_compare_dp812_successful_response_with_different_optional_params():
    """Compare DP812 successful responses with different optional params"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare DP812 responses for unknown client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3911", "User Story")
@scenario("Compare DP812 responses for unknown client")
def test_compare_dp812_successful_response_for_unknown_client():
    """Compare DP812 responses for unknown client"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return dp812_payload_setup(condition=conditions)


@given("I send the inquire provider request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP812", system="IIB", sub_system="MYMSD")
    response = api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])
    return response


@given("I send the inquire provider request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP812", system="AZURE")
    response = api_client.send_get_request(endpoint, headers=payload[0], params=payload[1], raise_on_error=False)
    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP812")
