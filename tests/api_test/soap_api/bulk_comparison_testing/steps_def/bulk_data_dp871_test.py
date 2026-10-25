from pytest_bdd import given, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp871_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for DP871
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for DP871")
def test_verify_bulk_client_data_dp871(batch_data):
    """test_verify_bulk_client_data_DP871"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for DP871", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    return dp871_payload_setup("update_communication_method_only", bulk_test=True, bulk_swn=str(batch_data))


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of DP871 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP871", system="IIB", sub_system="MYMSD")

    endpoint = f'{endpoint}?transactionId=' f'{payload["params"]["transactionId"]}'

    return api_client.send_rest_put_request(endpoint, payload["request_body"], payload["header"])


@when("I send the request of DP871 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP871", system="AZURE")

    endpoint = f'{endpoint}?transactionId=' f'{payload["params"]["transactionId"]}'

    return api_client.send_rest_put_request(endpoint, payload["request_body"], payload["header"])


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP871")
def then_i_can_see_all_the_responses_are_identical(api_client, response_iib, azure_responses, batch_data):
    api_client.compare_json_responses(response_iib[0], azure_responses[0], "DP871", bulk_test=True, bulk_swn=batch_data)
