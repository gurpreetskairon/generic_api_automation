from pytest_bdd import given, then, when

from utils.api_utils.helper.payload_setup import build_api_endpoint, sc829_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for SC829
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for SC829")
def test_verify_bulk_client_data_sc829(batch_data):
    """test_verify_bulk_client_data_SC829"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for SC829", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    if batch_data is None:
        raise AssertionError("SC829 bulk data setup failed: batch_data is None")

    payload = sc829_payload_setup(
        system="STAR", category_code="STAFFSECURITYALERT", type_code="TREP", client_identifier=str(batch_data)
    )

    request_body = payload.get("request_body")
    header = payload.get("header")

    if request_body is None:
        raise AssertionError("SC829 bulk data setup failed: request_body is None")

    if header is None:
        raise AssertionError("SC829 bulk data setup failed: header is None")

    if isinstance(request_body, bytes):
        request_body = request_body.decode("utf-8")

    return {
        "iib_headers": header,
        "iib_body": request_body,
        "azure_headers": header,
        "azure_body": request_body,
        "client_id": str(batch_data),
    }


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of SC829 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC829", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["iib_body"], headers=payload["iib_headers"])


@when("I send the request of SC829 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC829", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["azure_body"], headers=payload["azure_headers"])


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC829")
def then_i_can_see_all_the_responses_are_identical_for_sc829(api_client, response_iib, azure_responses, payload):
    api_client.compare_soap_responses(
        response_iib, azure_responses, "SC829", ignore_element_order=True, bulk_test=True, bulk_swn=payload["client_id"]
    )
