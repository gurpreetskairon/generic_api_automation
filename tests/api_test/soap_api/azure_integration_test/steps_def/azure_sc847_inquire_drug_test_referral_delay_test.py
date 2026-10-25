import os
from types import SimpleNamespace
from typing import cast

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc847_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


@pytest.mark.skip(reason="need to find new data")
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check SC847 inquireDrugTestReferralDelayResponse schema
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3150", "User Story")
@scenario("Check SC847 inquireDrugTestReferralDelayResponse schema")
def test_check_sc847_inquire_drug_test_referral_delay_response_schema():
    """Check SC847 inquireDrugTestReferralDelayResponse schema"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check SC847 successful Drug Test Referral Delay details
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3150", "User Story")
@scenario("Check SC847 successful Drug Test Referral Delay details")
def test_check_sc847_successful_drug_test_referral_delay_details():
    """Check SC847 successful Drug Test Referral Delay details"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check no matching record response when client has no active Drug Test Referral Delay
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3150", "User Story")
@scenario("Check SC847 no matching record response when client has no active Drug Test Referral Delay")
def test_check_sc847_no_matching_record_response_when_client_has_no_active_drug_test_referral_delay():
    """Check SC847 no matching record response when client has no active Drug Test Referral Delay"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I created the correct SC847 api payload", target_fixture="payload")
def create_correct_sc847_payload():
    return sc847_payload_setup()


@given(parsers.parse("I created the correct SC847 api payload for {dtrd_condition}"), target_fixture="payload")
def create_correct_sc847_payload_for_dtrd_condition(dtrd_condition):
    return sc847_payload_setup(dtrd_condition)


@given(parsers.parse("I created the SC847 api payload for {negative_condition}"), target_fixture="payload")
def create_sc847_payload_for_negative_condition(negative_condition):
    return sc847_payload_setup(negative_condition)


@given("I sent the inquire drug test referral delay request to the Azure endpoint", target_fixture="response")
def send_inquire_drug_test_referral_delay_request_to_azure_endpoint(api_client, payload):
    azure_pipeline_env = os.getenv("ENVIRONMENT_NAME")
    sc847_endpoint = build_api_endpoint("SC847", system="AZURE")

    if (azure_pipeline_env or "").casefold() == "sit":
        sc847_endpoint = cast(str, sc847_endpoint).replace("dev", "sit")

    return api_client.send_post_request(sc847_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the Transaction Successful returned")
def verify_transaction_successful_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, "Transaction Successful")


@then("I can see the No matching record returned")
def verify_no_matching_record_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, "No matching record")


@then("I can see the request auditId and transactionId returned in SOAP response header")
def verify_request_audit_id_and_transaction_id_returned(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.audit_id, payload["audit_id"])


@then("I can see the clientNumber and result code 84700 returned in the response SOAP header serviceResult")
def verify_client_number_and_result_code_84700_returned(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_number, payload["client_id"])

    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, "84700")


@then("I can see the clientNumber returned in the response SOAP header serviceResult")
def verify_client_number_returned_in_response_header_service_result(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_number, payload["client_id"])


@then(parsers.parse("I can see the result code {result_code} returned in the response SOAP header serviceResult"))
def verify_result_code_returned_in_response_header_service_result(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then('I can see Drug Test Referral Delay category code "DRUGTESTREFERRALDELAY" returned')
def verify_drug_test_referral_delay_category_code_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.dtrd_category_code, "DRUGTESTREFERRALDELAY")


@then('I can see Drug Test Referral Delay category description "Drug Test - Referral Delay" returned')
def verify_drug_test_referral_delay_category_description_returned(api_client, response):
    api_client.check_value_in_xml_response(
        response, dot_xml_pattern.dtrd_category_description, "Drug Test - Referral Delay"
    )


@then(parsers.parse('I can see Drug Test Referral Delay type code "{type_code}" returned'))
def verify_drug_test_referral_delay_type_code_returned(api_client, response, type_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.dtrd_type_code, type_code)


@then(parsers.parse('I can see Drug Test Referral Delay type description "{type_description}" returned'))
def verify_drug_test_referral_delay_type_description_returned(api_client, response, type_description):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.dtrd_type_description, type_description)


@then("I can see Drug Test Referral Delay effective start date returned")
def verify_drug_test_referral_delay_effective_start_date_returned(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.dtrd_effective_start, payload["effective_start"])


@then("I can see application error returned in the SOAP response")
def verify_application_error_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.exception_message, "Application error")


@then(parsers.parse("I can see result code {result_code} returned"))
def verify_result_code_returned(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see result message "{result_message}" returned'))
def verify_result_message_returned(api_client, response, result_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, result_message)


@then(parsers.parse("I can see exception code {exception_code} returned"))
def verify_exception_code_returned(api_client, response, exception_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.exception_code, exception_code)


@then(parsers.parse('I can see exception message "{exception_message}" returned'))
def verify_exception_message_returned(api_client, response, exception_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.exception_message, exception_message)
