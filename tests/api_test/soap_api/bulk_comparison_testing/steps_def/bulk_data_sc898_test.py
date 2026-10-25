import os

from pytest_bdd import given, then, when

from utils.api_utils.helper.payload_setup import build_api_endpoint, sc898_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for SC898
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for SC898")
def test_verify_bulk_client_data_sc898(batch_data):
    """test_verify_bulk_client_data_SC898"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for SC898", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    return sc898_payload_setup("active_c2e_flag", bulk_test=True, bulk_swn=str(batch_data))


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the SC898 request to both Azure and IIB endpoints", target_fixture="response")
def when_i_send_the_request_to_endpoints(api_client, payload):
    azure_pipeline_env = os.getenv("ENVIRONMENT_NAME", "")

    sc898_azure_endpoint = build_api_endpoint("SC898", system="AZURE")
    sc898_iib_endpoint = build_api_endpoint("SC898", system="IIB")

    if azure_pipeline_env.casefold() == "sit":
        sc898_azure_endpoint = sc898_azure_endpoint.replace("dev", "sit")
        sc898_iib_endpoint = sc898_iib_endpoint.replace("dev", "sit")

    azure_response = api_client.send_post_request(
        sc898_azure_endpoint, payload=payload["request_body"], headers=payload["header"]
    )
    iib_response = api_client.send_post_request(
        sc898_iib_endpoint, payload=payload["request_body"], headers=payload["header"]
    )

    return {"azure_response": azure_response, "iib_response": iib_response}


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC898")
def then_i_can_see_all_the_responses_are_identical_for_sc898(api_client, response, batch_data):
    api_client.compare_soap_responses(
        response["iib_response"],
        response["azure_response"],
        "SC898",
        bulk_test=True,
        bulk_swn=batch_data,
        ignore_tags=["correlationId"]
    )
