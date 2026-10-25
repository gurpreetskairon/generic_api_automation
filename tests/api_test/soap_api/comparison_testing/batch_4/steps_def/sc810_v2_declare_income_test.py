import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc810v2_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC810V2 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4282", "API-4282")
@scenario("Compare SC810V2 successful transaction response")
def test_compare_sc810v2_successful_transaction_response():
    """Compare SC810V2 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC810V2 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4282", "API-4282")
@scenario("Compare SC810V2 unsuccessful transaction responses")
def test_compare_sc810v2_unsuccessful_transaction_responses():
    """Compare SC810V2 unsuccessful transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given - Create payload
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC810V2 api payload with different {conditions}"), target_fixture="payload")
def create_sc810v2_payload_with_condition(conditions):
    return sc810v2_payload_setup(conditions)


# ══════════════════════════════════════════════════════════════════════════════
# Given - Send request to IIB
# ══════════════════════════════════════════════════════════════════════════════
@given("I send the SC810V2 request to IIB endpoint", target_fixture="response_iib")
def send_sc810v2_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC810V2", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["iib_request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Given - Send request to Azure
# ══════════════════════════════════════════════════════════════════════════════
@given("I send the SC810V2 request to Azure endpoint", target_fixture="response_azure")
def send_sc810v2_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC810V2", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["azure_request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then - Compare IIB and Azure responses
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC810V2")
def compare_all_sc810v2_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC810V2", ignore_tags=["objectRef"])
