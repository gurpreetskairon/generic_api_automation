from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc871_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC871 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3394", "API-3394")
@scenario("Compare SC871 successful transaction response")
def test_compare_sc871_successful_transaction_response():
    """Compare SC871 successful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC871 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3394", "API-3394")
@scenario("Compare SC871 unsuccessful transaction response")
def test_compare_sc871_unsuccessful_transaction_response():
    """Compare SC871 unsuccessful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the SC871 comparison payload for "{condition}"'), target_fixture="payload")
def create_sc871_comparison_payload(condition):
    return sc871_payload_setup(condition)


@given("I send the SC871 request to Azure endpoint", target_fixture="azure_response")
def send_sc871_request_to_azure(api_client, payload):
    azure_endpoint = build_api_endpoint("SC871", system="AZURE")

    return api_client.send_post_request(azure_endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC871 request to IIB endpoint", target_fixture="iib_response")
def send_sc871_request_to_iib(api_client, payload):
    iib_endpoint = build_api_endpoint("SC871", system="IIB")

    return api_client.send_post_request(iib_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC871")
def compare_all_responses(api_client, iib_response, azure_response):
    api_client.compare_soap_responses(iib_response[0], azure_response[0], "SC871")
