from pytest_bdd import given, then, when

from tests.api_test.soap_api.comparison_testing.steps_def import sc899_inquire_smoothed_income_test
from utils.api_utils.helper.payload_setup import sc899_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for SC899
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for SC899")
def test_verify_bulk_client_data_sc899(batch_data):
    """test_verify_bulk_client_data_SC899"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for SC899", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    return sc899_payload_setup(bulk_test=True, bulk_swn=batch_data)


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of SC899 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload):
    return sc899_inquire_smoothed_income_test.send_inquire_participant_request_for_client_tags_and_flags_to_iib(
        api_client, payload
    )


@when("I send the request of SC899 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload):
    return sc899_inquire_smoothed_income_test.send_inquire_participant_request_for_client_tags_and_flags_to_azure(
        api_client, payload
    )


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC899")
def then_i_can_see_all_the_responses_are_identical(api_client, response_iib, azure_responses, batch_data):
    api_client.compare_soap_responses(response_iib[0], azure_responses[0], "SC899", bulk_test=True, bulk_swn=batch_data)
