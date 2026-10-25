import os
from datetime import datetime
from types import SimpleNamespace
from typing import cast

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc898_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check SC898 inquireEligibilityResponse schema
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3060", "User Story")
@scenario("Check SC898 inquireEligibilityResponse schema")
def test_check_sc898_inquire_eligibility_response_schema():
    """Check SC898 inquireEligibilityResponse schema"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check SC898 successful Click to Enrol eligibility details
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3060", "User Story")
@scenario("Check SC898 successful Click to Enrol eligibility details")
def test_check_sc898_successful_click_to_enrol_eligibility_details():
    """Check SC898 successful Click to Enrol eligibility details"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check SC898 negative business result code and message
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3060", "User Story")
@scenario("Check SC898 negative business result code and message")
def test_check_sc898_negative_business_result_code_and_message():
    """Check SC898 negative business result code and message"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I created the correct SC898 api payload", target_fixture="payload")
def create_correct_sc898_payload():
    return sc898_payload_setup()


@given(parsers.parse("I created the correct SC898 api payload for {client_flag_condition}"), target_fixture="payload")
def create_correct_sc898_payload_for_client_flag_condition(client_flag_condition):
    return sc898_payload_setup(client_flag_condition)


@given(parsers.parse("I created the SC898 api payload for {negative_condition}"), target_fixture="payload")
def create_sc898_payload_for_negative_condition(negative_condition):
    return sc898_payload_setup(negative_condition)


@given("I sent the inquire eligibility request to the Azure endpoint", target_fixture="response")
def send_inquire_eligibility_request_to_azure_endpoint(api_client, payload):
    azure_pipeline_env = os.getenv("ENVIRONMENT_NAME")
    sc898_endpoint = build_api_endpoint("SC898", system="AZURE")

    if azure_pipeline_env and azure_pipeline_env.casefold() == "sit":
        sc898_endpoint = sc898_endpoint.replace("dev", "sit")

    return api_client.send_post_request(sc898_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the Transaction Successful returned")
def verify_status_message(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, "Transaction Successful")


@then("I can see the request auditId, requestDateTime and transactionId returned in SOAP response header")
def verify_request_header_details_returned(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.audit_id, payload["audit_id"])

    expected_request_date_time = datetime.strptime(payload["request_date_time"], "%Y-%m-%dT%H:%M:%S%z").strftime(
        "%Y%m%dT%H%M%S"
    )

    api_client.check_value_in_xml_response(response, dot_xml_pattern.request_datetime, expected_request_date_time)


@then("I can see the clientNumber and result code 89800 returned in the response SOAP header serviceResult")
def verify_client_number_and_result_code_89800_returned(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_number, payload["client_id"])

    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, "89800")


@then(parsers.parse("I can see the result code {result_code} returned in the response SOAP header serviceResult"))
def verify_result_code_returned_in_response_header_service_result(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see Click to Enrol flag code "{flag_code}" returned'))
def verify_click_to_enrol_flag_code_returned(api_client, response, flag_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_flag_code, flag_code)


@then(parsers.parse('I can see Click to Enrol flag description "{flag_description}" returned'))
def verify_click_to_enrol_flag_description_returned(api_client, response, flag_description):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_flag_description, flag_description)


@then(parsers.parse('I can see Click to Enrol status "{status}" returned'))
def verify_click_to_enrol_status_returned(api_client, response, status):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_flag_status, status)


@then(parsers.parse("I can see result code {result_code} returned"))
def verify_result_code(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see result message "{result_message}" returned'))
def verify_result_message(api_client, response, result_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, result_message)


@then(parsers.parse("I can see exception code {exception_code} returned"))
def verify_exception_code_returned(api_client, response, exception_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.exception_code, exception_code)


@then(parsers.parse('I can see exception message "{exception_message}" returned'))
def verify_exception_message_returned(api_client, response, exception_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.exception_message, exception_message)
