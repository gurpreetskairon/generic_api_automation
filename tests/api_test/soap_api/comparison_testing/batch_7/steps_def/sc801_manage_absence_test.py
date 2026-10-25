import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc801_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC801 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4621", "API-4621")
@scenario("Compare SC801 successful responses between IIB and Azure")
def test_compare_sc801_successful_transaction_response():
    """Compare SC801 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC801 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4621", "API-4621")
@scenario("Compare SC801 unsuccessful responses between IIB and Azure")
def test_compare_sc801_unsuccessful_transaction_response():
    """Compare SC801 unsuccessful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC801 api payload for {condition}"), target_fixture="payload")
def create_sc801_payload_with_condition(condition):
    return sc801_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC801 request to IIB endpoint", target_fixture="response_iib")
def send_sc801_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC801", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC801 request to Azure endpoint", target_fixture="response_azure")
def send_sc801_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC801", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC801")
def compare_all_sc801_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC801")
