import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc832_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC832 dispatch message responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4321", "User Story")
@scenario("Compare SC832 dispatch message responses")
def test_compare_sc832_dispatch_message_responses():
    """Compare SC832 dispatch message responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC832 api payload with {conditions}"), target_fixture="payload")
def create_sc832_payload_with_condition(conditions):
    return sc832_payload_setup(conditions)


@given("I send the SC832 request to IIB endpoint", target_fixture="response_iib")
def send_sc832_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC832", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC832 request to Azure endpoint", target_fixture="response_azure")
def send_sc832_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC832", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC832")
def compare_all_sc832_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC832")
