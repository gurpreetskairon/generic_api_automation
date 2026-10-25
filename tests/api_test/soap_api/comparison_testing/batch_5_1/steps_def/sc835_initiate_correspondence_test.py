import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc835_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC835 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4319", "User Story")
@scenario("Compare SC835 successful transaction response")
def test_compare_sc835_successful_transaction_response():
    """Compare SC835 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC835 no matching template response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4319", "User Story")
@scenario("Compare SC835 no matching template response")
def test_compare_sc835_no_matching_template_response():
    """Compare SC835 no matching template response."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC835 api payload with different {conditions}"), target_fixture="payload")
def create_sc835_payload_with_condition(conditions):
    return sc835_payload_setup(conditions)


@given("I send the SC835 request to IIB endpoint", target_fixture="response_iib")
def send_sc835_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC835", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC835 request to Azure endpoint", target_fixture="response_azure")
def send_sc835_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC835", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC835")
def compare_all_sc835_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC835")
