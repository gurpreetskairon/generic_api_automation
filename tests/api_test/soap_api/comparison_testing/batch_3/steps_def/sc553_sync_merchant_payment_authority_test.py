from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc553_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC553 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@scenario("Compare SC553 successful transaction response")
def test_compare_sc553_successful_transaction_response():
    """Compare SC553 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC553 unsuccessful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@scenario("Compare SC553 unsuccessful transaction responses")
def test_compare_sc553_unsuccessful_transaction_responses():
    """Compare SC553 unsuccessful transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC553 api payload with different {conditions}"), target_fixture="payload")
def create_sc553_payload_with_condition(conditions):
    return sc553_payload_setup(conditions)


@given("I send the SC553 request to IIB endpoint", target_fixture="response_iib")
def send_sc553_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC553", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC553 request to Azure endpoint", target_fixture="response_azure")
def send_sc553_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC553", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC553")
def compare_all_sc553_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC553")
