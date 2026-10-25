import os
from types import SimpleNamespace
from typing import cast

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc828_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check SC828 inquireParticipantResponse schema for successful transaction
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Check SC828 inquireParticipantResponse schema for successful transaction")
def test_check_sc828_response_schema():
    """Check the SC828 inquireParticipantResponse schema for successful transaction"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check SC828 successful transaction matched client details
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Check SC828 successful transaction matched client details")
def test_check_sc828_successful_transaction_matched_client_details():
    """Check SC828 successful transaction matched client details"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check returns matched client details for supported special client record types
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Check SC828 returns matched client details for supported special client record types")
def test_check_sc828_returns_matched_client_details_for_supported_special_client_record_types():
    """Check SC828 returns matched client details for supported special client record types"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Check SC828 no matching record result code and message
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Check SC828 no matching record result code and message")
def test_check_sc828_no_matching_record_result_code_and_message():
    """Check SC828 no matching record result code and message"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Check SC828 invalid request for too short client name
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Check SC828 invalid request for too short client name")
def test_check_sc828_invalid_request_for_too_short_client_name():
    """Check SC828 invalid request for too short client name"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Check SC828 invalid request when date of birth is missing from request
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2847", "User Story")
@scenario("Check SC828 invalid request when date of birth is missing from request")
def test_check_sc828_invalid_request_when_date_of_birth_is_missing_from_request():
    """Check SC828 invalid request when date of birth is missing from request"""


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


@given("I sent the inquire participant request to the Azure endpoint", target_fixture="response")
def send_inquire_participant_request(api_client, payload):
    azure_pipeline_env = os.getenv("ENVIRONMENT_NAME")

    sc828_endpoint = build_api_endpoint("SC828", system="AZURE")

    if azure_pipeline_env and azure_pipeline_env.casefold() == "sit":
        sc828_endpoint = str, sc828_endpoint.replace("dev", "sit")

    return api_client.send_post_request(sc828_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the Transaction Successful returned")
def verify_status_message(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, "Transaction Successful")


@then("I can see the request auditId, requestDateTime and transactionId returned in SOAP response header")
def verify_header_response(api_client, response, payload):
    api_client.check_datetime_is_not_none(response, dot_xml_pattern.request_datetime)

    api_client.check_value_from_payload(
        response, dot_xml_pattern.audit_id, payload["request_body"], dot_xml_pattern.audit_id, check_name="audit id"
    )

    api_client.check_value_from_payload(
        response,
        dot_xml_pattern.transaction_id,
        payload["request_body"],
        dot_xml_pattern.transaction_id,
        check_name="transaction id"
    )


@then("I can see the response messageType returned as RESPONSE")
def verify_response_message_type(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.message_type, "RESPONSE")


@then("I can see the result code 82800 returned in the response SOAP header serviceResult")
def verify_result_code_82800(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, "82800")


@then('I can see the result message "Transaction Successful" returned in the response SOAP header serviceResult')
def verify_result_message_transaction_successful(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, "Transaction Successful")


@then("I can see the detail of the matched client returned in the response")
def verify_matched_client_details_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "identityMatchList", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "identityMatch", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "participant", is_check_equal=False)


@then(parsers.parse("I can see nameConfidenceLevel {name_confidence_level} returned in the response"))
def verify_name_confidence_level(api_client, response, name_confidence_level):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.name_confidence_level, name_confidence_level)


@then(parsers.parse("I can see dateOfBirthConfidenceLevel {date_of_birth_confidence_level} returned in the response"))
def verify_date_of_birth_confidence_level(api_client, response, date_of_birth_confidence_level):
    api_client.check_value_in_xml_response(
        response, dot_xml_pattern.date_of_birth_confidence_level, date_of_birth_confidence_level
    )


@then("I can see clientExistsInSWIFTT returned in the response")
def verify_client_exists_in_swiftt_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "clientExistsInSWIFTT", is_check_equal=False)


@then("I can see matched client details returned in the response")
def verify_matched_client_details_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "participant", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "businessKey", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "name", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "person", is_check_equal=False)


@then(
    "I can see client number, first name, family name, middle names, date of birth and gender returned in the response"
)
def verify_client_identity_fields_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "CLIENTNUMBER", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "familyName", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "firstName", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "middleNames", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "dateOfBirth", is_check_equal=False)

    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "gender", is_check_equal=False)


@then(parsers.parse("I can see result code {result_code} returned"))
def verify_result_code(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see result message "{result_message}" returned'))
def verify_result_message(api_client, response, result_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, result_message)


@then("I cannot see identityMatch returned in the response")
def verify_identity_match_not_returned(api_client, response):
    api_client.check_value_in_xml_response(
        response, dot_xml_pattern.body, "identityMatch", is_check_equal=False, is_should_exist=False
    )


@then("I can see businessKey returned in the participant response")
def verify_business_key_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "businessKey", is_check_equal=False)


@then("I can see identifier returned in the businessKey response")
def verify_business_key_identifier_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "identifier", is_check_equal=False)


@then('I can see businessKey type code "CLIENTNUMBER" returned in the response')
def verify_business_key_type_code_client_number(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.body, "CLIENTNUMBER", is_check_equal=False)
