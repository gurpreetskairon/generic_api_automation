import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc901_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC901 successful declare income responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3620", "User Story")
@scenario("Compare SC901 successful declare income responses")
def test_compare_sc901_successful_declare_income_responses():
    """Compare successful new and updated income declaration responses from IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC901 unrecognised income master-data responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3620", "User Story")
@scenario("Compare SC901 responses for unrecognised income master data")
def test_compare_sc901_unrecognised_income_master_data_responses():
    """Compare unrecognised income master-data responses from IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC901 api payload for {condition}"), target_fixture="payload")
def create_sc901_payload_for_condition(condition):
    return sc901_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC901 declare income request to IIB endpoint", target_fixture="response_iib")
def send_sc901_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC901", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC901 declare income request to Azure endpoint", target_fixture="response_azure")
def send_sc901_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC901", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC901")
def compare_sc901_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC901", ignore_element_order=True)
