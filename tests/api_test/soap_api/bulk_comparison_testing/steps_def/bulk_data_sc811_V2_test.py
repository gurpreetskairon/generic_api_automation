from pytest_bdd import given, then, when

from tests.api_test.soap_api.comparison_testing.steps_def import sc811_v2_inquire_circumstance_test
from utils.api_utils.helper.payload_setup import sc811_v2_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for SC811_V2
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for SC811_V2")
def test_verify_bulk_client_data_sc811_v2(batch_data):
    """test_verify_bulk_client_data_SC811_V2"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for SC811_V2", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    return sc811_v2_payload_setup("success", bulk_test=True, bulk_swn=batch_data)


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of SC811_V2 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload):
    return sc811_v2_inquire_circumstance_test.send_iib_request(api_client, payload)


@when("I send the request of SC811_V2 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload):
    return sc811_v2_inquire_circumstance_test.send_azure_request(api_client, payload)


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC811_V2")
def then_i_can_see_all_the_responses_are_identical(api_client, response_iib, azure_responses, batch_data):
    api_client.compare_soap_responses(
        response_iib[0], azure_responses[0], "SC811_V2", bulk_test=True, bulk_swn=batch_data
    )
