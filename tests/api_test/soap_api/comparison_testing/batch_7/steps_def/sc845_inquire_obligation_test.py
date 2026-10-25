import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc845_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC845 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4195", "User Story")
@scenario("Compare SC845 successful responses between IIB and Azure")
def test_compare_sc845_successful_responses():
    """Compare SC845 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC845 api payload for {condition}"), target_fixture="payload")
def create_sc845_payload(condition):
    return sc845_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC845 request to IIB endpoint", target_fixture="response_iib")
def send_sc845_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC845", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0], raise_error=False)


@when("I send SC845 request to Azure endpoint", target_fixture="response_azure")
def send_sc845_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC845", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0], raise_error=False)


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC845")
def compare_sc845_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC845", ignore_element_order=True)
