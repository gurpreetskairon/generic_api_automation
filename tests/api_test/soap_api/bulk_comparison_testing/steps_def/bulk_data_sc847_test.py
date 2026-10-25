from pytest_bdd import given, then, when

from tests.api_test.soap_api.comparison_testing.steps_def import sc847_inquire_drug_test_referral_delay_test
from utils.api_utils.helper.payload_setup import sc847_payload_setup
from utils.bdd_utils.scenario import scenario


# ════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify bulk client data for SC847
# ════════════════════════════════════════════════════════════════════════════
@scenario("Verify bulk client data for SC847")
def test_verify_bulk_client_data_sc847(batch_data):
    """test_verify_bulk_client_data_SC847"""


# ════════════════════════════════════════════════════════════════════════════
# Given steps
# ════════════════════════════════════════════════════════════════════════════
@given("I have updated payloads with the bulk data for SC847", target_fixture="payload")
def given_update_payloads_with_bulk_data(batch_data):
    return sc847_payload_setup("dtrd_prescription_medication", bulk_test=True, bulk_swn=batch_data)


# ════════════════════════════════════════════════════════════════════════════
# When steps
# ════════════════════════════════════════════════════════════════════════════
@when("I send the SC847 request to both Azure and IIB endpoints", target_fixture="responses")
def when_i_send_the_request_to_both_endpoints(api_client, payload):
    return sc847_inquire_drug_test_referral_delay_test.send_sc847_request_to_both_azure_and_iib_endpoints(
        api_client, payload
    )


# ════════════════════════════════════════════════════════════════════════════
# Then steps
# ════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC847")
def then_i_can_see_all_the_responses_are_identical(api_client, responses, batch_data):
    api_client.compare_soap_responses(
        responses["iib_response"][0], responses["azure_response"][0], "SC847", bulk_test=True, bulk_swn=batch_data
    )
