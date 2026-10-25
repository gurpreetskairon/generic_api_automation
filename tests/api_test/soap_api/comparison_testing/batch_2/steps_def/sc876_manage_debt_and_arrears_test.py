from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc876_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC876 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3616", "API-3616")
@scenario("Compare SC876 successful transaction response")
def test_compare_sc876_successful_transaction_response():
    """Compare SC876 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC876 unsuccessful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3616", "API-3616")
@scenario("Compare SC876 unsuccessful transaction responses")
def test_compare_sc876_unsuccessful_transaction_responses():
    """Compare SC876 unsuccessful transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC876 api payload with different {conditions}"), target_fixture="payload")
def create_sc876_payload_with_condition(conditions):
    return sc876_payload_setup(conditions)


@given("I send the SC876 request to IIB endpoint", target_fixture="response_iib")
def send_sc876_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC876", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC876 request to Azure endpoint", target_fixture="response_azure")
def send_sc876_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC876", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC876")
def compare_all_sc876_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC876")
