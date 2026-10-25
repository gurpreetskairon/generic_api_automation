from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc811_v1_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC811 V1 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3156", "API-3156")
@scenario("Compare SC811 V1 successful transaction response")
def test_compare_sc811_v1_successful_transaction_response():
    """Compare SC811 V1 successful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC811 V1 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3156", "API-3156")
@scenario("Compare SC811 V1 unsuccessful transaction response")
def test_compare_sc811_v1_unsuccessful_transaction_response():
    """Compare SC811 V1 unsuccessful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the correct payload for SC811 V1 with "{condition}"'), target_fixture="payload")
def create_correct_payload(condition):
    return sc811_v1_payload_setup(condition)


@given(parsers.parse('I create the payload for SC811 V1 with "{condition}"'), target_fixture="payload")
def create_payload(condition):
    return sc811_v1_payload_setup(condition)


@given("I send the SC811 V1 request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC811V1", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC811 V1 request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC811V1", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC811 V1")
def compare_all_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC811V1")
