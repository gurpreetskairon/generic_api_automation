from pytest_bdd import given, then, when

from apps.services.integration_soap.payload_data.dp603 import url_azure, url_iib
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp603_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for DP603
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for DP603")
def test_verify_bulk_client_data_dp603(batch_data):
    """test_verify_bulk_client_data_dp603"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for DP603", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    iib_payload = dp603_payload_setup(swn=str(batch_data))
    azure_payload = dp603_payload_setup(swn=str(batch_data), azure=True)
    return {"iib_headers": iib_payload, "azure_headers": azure_payload}


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of DP603 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload, batch_data):
    endpoint = build_api_endpoint("DP603", system="IIB", sub_system="STAR")
    return api_client.send_get_request(
        url_iib(endpoint, payload, swn=str(batch_data)), headers=payload["iib_headers"], raise_on_error=False
    )


@when("I send the request of DP603 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload, batch_data):
    endpoint = build_api_endpoint("DP603", system="AZURE")
    return api_client.send_get_request(
        url_azure(endpoint, payload, swn=str(batch_data)), headers=payload["azure_headers"], raise_on_error=False
    )


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP603")
def then_i_can_see_all_the_responses_are_identical(api_client, response_iib, azure_responses, batch_data):
    api_client.compare_json_responses(response_iib[0], azure_responses[0], "DP603", bulk_test=True, bulk_swn=batch_data)
