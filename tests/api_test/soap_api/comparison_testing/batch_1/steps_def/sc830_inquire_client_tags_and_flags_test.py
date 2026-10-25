import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.payload_setup import build_api_endpoint, sc830_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare successful response when client has programme tags and client flags
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Compare SC830 successful response when client has programme tags and client flags")
def test_compare_sc830_successful_response_when_client_has_programme_tags_and_client_flags():
    """Compare SC830 successful response when client has programme tags and client flags"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC830 successful result and subresult
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Compare SC830 successful result and subresult")
def test_compare_sc830_successful_result_and_subresult():
    """Compare SC830 successful result and subresult"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC830 responses when the client or user cannot be validated
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Compare SC830 responses when the client or user cannot be validated")
def test_compare_sc830_responses_when_the_client_or_user_cannot_be_validated():
    """Compare SC830 responses when the client or user cannot be validated"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc830_payload_setup()


@given(parsers.parse("I create the correct api payload for {client_type}"), target_fixture="payload")
def create_correct_payload_for_client_type(client_type):
    return sc830_payload_setup(client_type)


@given(parsers.parse("I create the api payload for {condition}"), target_fixture="payload")
def create_payload_for_condition(condition):
    return sc830_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send inquire participant request for client tags and flags to IIB endpoint", target_fixture="iib_response")
def send_inquire_participant_request_for_client_tags_and_flags_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC830", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send inquire participant request for client tags and flags to Azure endpoint", target_fixture="azure_response")
def send_inquire_participant_request_for_client_tags_and_flags_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC830", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC830")
def then_i_can_see_all_the_responses_are_identical_for_sc830(api_client, iib_response, azure_response):
    api_client.compare_soap_responses(iib_response, azure_response, "SC830", ignore_element_order=True)
