import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc874_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC874 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4278", "API-4278")
@scenario("Compare SC874 successful transaction response")
def test_compare_sc874_successful_transaction_response():
    """Compare SC874 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC874 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4278", "API-4278")
@scenario("Compare SC874 unsuccessful transaction response")
def test_compare_sc874_unsuccessful_transaction_response():
    """Compare SC874 unsuccessful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC874 api payload with different {conditions}"), target_fixture="payload")
def create_sc874_payload_with_condition(conditions):
    return sc874_payload_setup(conditions)


@given("I send the SC874 request to IIB endpoint", target_fixture="response_iib")
def send_sc874_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC874", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC874 request to Azure endpoint", target_fixture="response_azure")
def send_sc874_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC874", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC874")
def compare_all_sc874_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC874")
