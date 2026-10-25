from pytest_bdd import given, then, when

from utils.api_utils.helper.payload_setup import build_api_endpoint, sc830_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for SC830
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for SC830")
def test_verify_bulk_client_data_sc830(batch_data):
    """test_verify_bulk_client_data_SC830"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for SC830", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    return sc830_payload_setup(bulk_test=True, bulk_swn=str(batch_data))


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of SC830 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC830", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send the request of SC830 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC830", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC830")
def then_i_can_see_all_the_responses_are_identical(api_client, response_iib, azure_responses, payload):
    api_client.compare_soap_responses(
        response_iib, azure_responses, "SC830", ignore_element_order=True, bulk_test=True, bulk_swn=payload["client_id"]
    )
