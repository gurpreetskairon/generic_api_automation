import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc807_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC807 successful create debt and redirections responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3516", "User Story")
@scenario("Compare SC807 successful create debt and redirections responses")
def test_compare_sc807_successful_create_debt_and_redirections_responses():
    """Compare successful SC807 responses returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC807 unsuccessful and invalid request responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3516", "User Story")
@scenario("Compare SC807 unsuccessful and invalid request responses")
def test_compare_sc807_unsuccessful_and_invalid_request_responses():
    """Compare unsuccessful and invalid SC807 responses returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC807 api payload for {condition}"), target_fixture="payload")
def create_sc807_payload_for_condition(condition):
    return sc807_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC807 create debt and redirections request to IIB endpoint", target_fixture="response_iib")
def send_sc807_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC807", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC807 create debt and redirections request to Azure endpoint", target_fixture="response_azure")
def send_sc807_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC807", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC807")
def compare_sc807_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC807", ignore_element_order=True)
