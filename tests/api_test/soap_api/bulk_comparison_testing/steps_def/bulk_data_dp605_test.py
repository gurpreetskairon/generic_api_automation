from pytest_bdd import given, then, when
from utils.api_utils.helper.payload_setup import dp605_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for DP605
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for DP605")
def test_verify_bulk_client_data_dp605(batch_data):
    """test_verify_bulk_client_data_dp605"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for DP605", target_fixture="payload")
def given_update_payloads_with_bulk_data():
    return {"category_code": "STAFFSECURITYALERT", "type_code": "LWAR", "condition": "valid_client"}


@given("I used a valid client number as the DP605 path parameter")
def use_valid_client_number_as_dp605_path_parameter(payload):
    payload["condition"] = "valid_client"


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of DP605 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload, batch_data):
    iib_payload = dp605_payload_setup(
        condition=payload["condition"],
        category_code=payload["category_code"],
        type_code=payload["type_code"],
        system="IIB",
        subsystem="STAR",
        client_number=str(batch_data)
    )

    return api_client.send_post_request(
        iib_payload["endpoint_url"],
        payload=iib_payload["request_body"],
        headers=iib_payload["header"],
        json_payload=True
    )


@when("I send the request of DP605 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload, batch_data):
    azure_payload = dp605_payload_setup(
        condition=payload["condition"],
        category_code=payload["category_code"],
        type_code=payload["type_code"],
        system="AZURE",
        client_number=str(batch_data)
    )

    return api_client.send_post_request(
        azure_payload["endpoint_url"],
        payload=azure_payload["request_body"],
        headers=azure_payload["header"],
        json_payload=True
    )


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP605")
def then_i_can_see_all_the_responses_are_identical(api_client, response_iib, azure_responses, batch_data):
    api_client.compare_json_responses(response_iib[0], azure_responses[0], "DP605", bulk_test=True, bulk_swn=batch_data)
