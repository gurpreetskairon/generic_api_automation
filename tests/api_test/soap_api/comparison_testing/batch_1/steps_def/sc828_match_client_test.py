import os

import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc828_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC828 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Compare SC828 successful response")
def test_compare_sc828_successful_response():
    """Compare SC828 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC828 successful matched client confidence details
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Compare SC828 successful matched client confidence details")
def test_compare_sc828_successful_matched_client_confidence_details():
    """Compare SC828 successful matched client confidence details"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare matched client details for supported special client record types
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Compare SC828 matched client details for supported special client record types")
def test_compare_sc828_matched_client_details_for_supported_special_client_record_types():
    """Compare SC828 matched client details for supported special client record types"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC828 no matching record response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Compare SC828 no matching record response")
def test_compare_sc828_no_matching_record_response():
    """Compare SC828 no matching record response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Compare SC828 invalid request response for too short client name
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Compare SC828 invalid request response for too short client name")
def test_compare_sc828_invalid_request_response_for_too_short_client_name():
    """Compare SC828 invalid request response for too short client name"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 6 - Compare invalid request response when date of birth is missing from request
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Compare SC828 invalid request response when date of birth is missing from request")
def test_compare_sc828_invalid_request_response_when_date_of_birth_is_missing_from_request():
    """Compare SC828 invalid request response when date of birth is missing from request"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I created the correct SC828 api payload", target_fixture="payload")
def create_correct_sc828_payload():
    return sc828_payload_setup()


@given(parsers.parse("I created the correct SC828 api payload for {client_match_condition}"), target_fixture="payload")
def create_correct_sc828_payload_for_client_match_condition(client_match_condition):
    return sc828_payload_setup(client_match_condition)


@given(parsers.parse("I created the invalid SC828 api payload for {negative_condition}"), target_fixture="payload")
def create_invalid_sc828_payload(negative_condition):
    return sc828_payload_setup(negative_condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send inquire participant request to IIB endpoint", target_fixture="iib_response")
def send_inquire_participant_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC828", system="IIB")

    if os.getenv("ENVIRONMENT_NAME", "").casefold() == "sit":
        endpoint = endpoint.replace("dev", "sit")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send the inquire participant request to Azure endpoint", target_fixture="azure_response")
def send_inquire_participant_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC828", system="AZURE")

    if os.getenv("ENVIRONMENT_NAME", "").casefold() == "sit":
        endpoint = endpoint.replace("dev", "sit")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC828")
def then_i_can_see_all_the_responses_are_identical_for_sc828(api_client, iib_response, azure_response):
    api_client.compare_soap_responses(iib_response, azure_response, "SC828", ignore_element_order=True)
