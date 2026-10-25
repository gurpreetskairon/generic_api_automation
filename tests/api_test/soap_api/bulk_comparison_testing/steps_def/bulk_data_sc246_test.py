from pytest_bdd import given, then, when

from tests.api_test.soap_api.comparison_testing.steps_def import sc246_inquire_client_identity_verification_status_test
from utils.api_utils.helper.payload_setup import sc246_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for SC246
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for SC246")
def test_verify_bulk_client_data_sc246(batch_data):
    """test_verify_bulk_client_data_SC246"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for SC246", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data, formatted_datetime):
    iib_headers, iib_body = sc246_payload_setup(bulk_test=True, bulk_swn=batch_data, date_time=formatted_datetime)
    azure_headers, azure_body = sc246_payload_setup(bulk_test=True, bulk_swn=batch_data, date_time=formatted_datetime)
    return {"iib_headers": iib_headers, "iib_body": iib_body, "azure_headers": azure_headers, "azure_body": azure_body}


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the request of SC246 to IIB endpoint", target_fixture="response_iib")
def when_i_send_the_request_to_iib_endpoint(api_client, payload):
    return sc246_inquire_client_identity_verification_status_test.send_iib_request(api_client, payload)


@when("I send the request of SC246 to Azure endpoint", target_fixture="azure_responses")
def when_i_send_the_request_to_azure_endpoint(api_client, payload):
    return sc246_inquire_client_identity_verification_status_test.send_azure_request(api_client, payload)


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC246")
def then_i_can_see_all_the_responses_are_identical(api_client, response_iib, azure_responses, batch_data):
    api_client.compare_soap_responses(response_iib[0], azure_responses[0], "SC246", bulk_test=True, bulk_swn=batch_data)
