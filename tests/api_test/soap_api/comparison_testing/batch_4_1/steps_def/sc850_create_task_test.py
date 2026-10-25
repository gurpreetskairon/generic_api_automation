import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc850_payload_setup
from utils.bdd_utils.scenario import scenario


@pytest.mark.skip("The release date for this service has been delayed")
# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC850 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3617", "API-3617")
@scenario("Compare SC850 successful transaction response")
def test_compare_sc850_successful_transaction_response():
    """Compare SC850 successful transaction response."""


@pytest.mark.skip("The release date for this service has been delayed")
# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC850 api payload with different {conditions}"), target_fixture="payload")
def create_sc850_payload_with_condition(conditions):
    """Create the SC850 request headers and SOAP payload."""

    return sc850_payload_setup(conditions)


@given("I send the SC850 request to IIB endpoint", target_fixture="response_iib")
def send_sc850_request_to_iib_endpoint(api_client, payload):
    """Send the SC850 request to the IIB endpoint."""

    endpoint = build_api_endpoint("SC850", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC850 request to Azure endpoint", target_fixture="response_azure")
def send_sc850_request_to_azure_endpoint(api_client, payload):
    """Send the SC850 request to the Azure endpoint."""

    endpoint = build_api_endpoint("SC850", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC850")
def compare_all_sc850_responses(api_client, response_iib, response_azure):
    """Compare the SOAP responses returned by IIB and Azure."""

    api_client.compare_soap_responses(response_iib, response_azure, "SC850")
