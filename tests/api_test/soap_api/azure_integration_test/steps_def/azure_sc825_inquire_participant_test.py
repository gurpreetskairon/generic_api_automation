import os
from types import SimpleNamespace
from typing import cast

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc825_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check SC825 inquireParticipantResponse schema
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2912", "User Story")
@scenario("Check SC825 inquireParticipantResponse schema")
def test_check_sc825_response_schema():
    """Check the SC825 inquireParticipantResponse schema"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check SC825 LDAP exception response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2912", "User Story")
@scenario("Check SC825 LDAP exception response")
def test_check_sc825_ldap_exception_response():
    """Check the SC825 LDAP exception response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check SC825 successful transaction sub-result details
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2912", "User Story")
@scenario("Check SC825 successful transaction subresult details")
def test_check_sc825_successful_transaction_subresult_details():
    """Check SC825 successful transaction subresult details"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Check SC825 negative business result code and message
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2912", "User Story")
@scenario("Check SC825 negative business result code and message")
def test_check_sc825_negative_business_result_code_and_message():
    """Check SC825 negative business result code and message"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I created the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc825_payload_setup()


@given(parsers.parse("I created the api payload with an invalid {token}"), target_fixture="payload")
def create_correct_invalid_payload(token):
    return sc825_payload_setup(token)


@given("I sent the inquire participant request to the Azure endpoint", target_fixture="response")
@given("I sent the exceptional inquire participant request to the Azure endpoint", target_fixture="exception_response")
def send_inquire_participant_request(api_client, payload):
    azure_pipeline_env = os.getenv("ENVIRONMENT_NAME")
    sc825_endpoint = build_api_endpoint("SC825", system="AZURE")
    if azure_pipeline_env and azure_pipeline_env.casefold() == "sit":
        sc825_endpoint = sc825_endpoint.replace("dev", "sit")
    return api_client.send_post_request(sc825_endpoint, payload=payload["request_body"], headers=payload["header"])


@given(parsers.parse("I created the correct api payload for {client_type}"), target_fixture="payload")
def create_correct_payload_for_client_type(client_type):
    return sc825_payload_setup(client_type)


@given(parsers.parse("I created the api payload for {negative_condition}"), target_fixture="payload")
def create_negative_business_payload(negative_condition):
    return sc825_payload_setup(negative_condition)


def send_request_to_unavailable_azure_endpoint(api_client, payload):
    return api_client.send_post_request(
        os.getenv("SC825_UNAVAILABLE_AZURE_URL"), payload=payload["request_body"], headers=payload["header"]
    )


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


@then("I can see the clientNumber and result code 82500 returned in the response SOAP header serviceResult")
def verify_header_service_request(api_client, response, payload):
    api_client.check_value_from_payload(
        response,
        dot_xml_pattern.client_number,
        payload["request_body"],
        dot_xml_pattern.identifier,
        check_name="client Number"
    )
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, "82500")


@then("I can see the result code 82500 returned in the response SOAP header serviceResult")
def verify_result_code_82500(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, "82500")


@then(parsers.parse("I can see LDAP exception code {exception_code} returned"))
def verify_ldap_exception_code(api_client, exception_response, exception_code):
    api_client.check_value_in_xml_response(exception_response, dot_xml_pattern.exception_code, exception_code)


@then("I can see inquireParticipantException response schema returned")
def verify_exception_response_schema_returned(api_client, exception_response):
    api_client.check_value_in_xml_response(
        exception_response, dot_xml_pattern.body, "inquireParticipantException", is_check_equal=False
    )


@then(parsers.parse("I can see result code {result_code} returned"))
def verify_result_code(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see result message "{result_message}" returned'))
def verify_result_message(api_client, response, result_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, result_message)


@then(parsers.parse("I can see subresult code {subresult_code} returned"))
def verify_subresult_code(api_client, response, subresult_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.subresult_code, subresult_code)


@then(parsers.parse('I can see subresult message "{subresult_message}" returned'))
def verify_subresult_message(api_client, response, subresult_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.subresult_message, subresult_message)
