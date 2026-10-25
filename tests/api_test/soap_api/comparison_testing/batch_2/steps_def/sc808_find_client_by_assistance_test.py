import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc808_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC808 successful responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3623", "User Story")
@scenario("Compare SC808 successful responses")
def test_compare_sc808_successful_responses():
    """Compare successful SC808 responses returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC808 unsuccessful search responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3623", "User Story")
@scenario("Compare SC808 unsuccessful search responses")
def test_compare_sc808_unsuccessful_search_responses():
    """Compare unsuccessful SC808 search responses returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC808 api payload for {condition}"), target_fixture="payload")
def create_sc808_payload_for_condition(condition):
    return sc808_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC808 find client request to IIB endpoint", target_fixture="response_iib")
def send_sc808_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC808", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC808 find client request to Azure endpoint", target_fixture="response_azure")
def send_sc808_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC808", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC808")
def compare_sc808_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC808", ignore_element_order=True)
