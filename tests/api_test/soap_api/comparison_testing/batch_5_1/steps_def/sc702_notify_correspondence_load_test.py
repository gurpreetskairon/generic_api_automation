import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc702_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC702 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4326", "User Story")
@scenario("Compare SC702 successful transaction response")
def test_compare_sc702_successful_transaction_response():
    """Compare SC702 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC702 api payload with different {conditions}"), target_fixture="payload")
def create_sc702_payload_with_condition(conditions):
    return sc702_payload_setup(conditions)


@given("I send the SC702 request to IIB endpoint", target_fixture="response_iib")
def send_sc702_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC702", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC702 request to Azure endpoint", target_fixture="response_azure")
def send_sc702_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC702", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC702")
def compare_all_sc702_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC702")
