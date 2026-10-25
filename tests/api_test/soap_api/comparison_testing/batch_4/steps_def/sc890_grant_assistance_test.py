from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc890_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario - Successful transaction
# ══════════════════════════════════════════════════════════════════════════════
@scenario("Compare SC890 successful transaction response")
def test_compare_sc890_successful_transaction_response():
    """Compare SC890 responses from IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC890 api payload with different {conditions}"), target_fixture="payload")
def create_sc890_payload_with_condition(conditions):
    return sc890_payload_setup(conditions)


@given("I send the SC890 request to IIB endpoint", target_fixture="response_iib")
def send_sc890_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC890", system="IIB")

    response_iib = api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
    )

    print("IIB STATUS:", response_iib[1])
    print("IIB RESPONSE:", response_iib[0])

    return response_iib


@given("I send the SC890 request to Azure endpoint", target_fixture="response_azure")
def send_sc890_request_to_azure_endpoint(api_client, payload, response_iib):
    endpoint = build_api_endpoint("SC890", system="AZURE")

    response_azure = api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
    )

    return response_azure


# ══════════════════════════════════════════════════════════════════════════════
# Then step
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC890")
def compare_all_sc890_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC890", trim_message_whitespace=True)
