import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc868_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC868 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4254", "User Story")
@scenario("Compare SC868 successful transaction response")
def test_compare_sc868_successful_transaction_response():
    """Compare SC868 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC868 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4254", "User Story")
@scenario("Compare SC868 invalid request response")
def test_compare_sc868_invalid_request_response():
    """Compare SC868 invalid request response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC868 api payload with different {conditions}"), target_fixture="payload")
def create_sc868_payload_with_condition(conditions):
    return sc868_payload_setup(conditions)


@given("I send the SC868 request to IIB endpoint", target_fixture="response_iib")
def send_sc868_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC868", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC868 request to Azure endpoint", target_fixture="response_azure")
def send_sc868_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC868", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════

@then("I can see all the responses are identical for SC868")
def compare_all_sc868_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(
        response_iib,
        response_azure,
        "SC868",
        ignore_tags=["objectRef"]
    )
