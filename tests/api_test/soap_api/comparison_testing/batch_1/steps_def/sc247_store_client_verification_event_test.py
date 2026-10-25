from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc247_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC247 successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Compare SC247 successful responses")
def test_compare_sc247_successful_response():
    """Compare SC247 successful responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC247 responses for no matching clients
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Compare SC247 responses for no matching clients")
def test_compare_sc247_response_for_no_matching_clients():
    """Compare SC247 responses for no matching clients"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC247 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Compare SC247 responses with invalid data")
def test_compare_sc247_response_with_invalid_data():
    """Compare SC247 responses with invalid data"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC247 responses with an invalid client number
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Compare SC247 responses with an invalid client number")
def test_compare_sc247_response_with_invalid_client_number():
    """Compare SC247 responses with an invalid client number"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc247_payload_setup()


@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return sc247_payload_setup(conditions=conditions)


@given("I send the request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC247", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[0], headers=payload[1])


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC247", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[0], headers=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC247")
