from types import SimpleNamespace

import allure
import pytest
import requests
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc875_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check SC875 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3173", "API-3173")
@scenario("Check SC875 successful transaction response")
def test_sc875_successful_transaction_response():
    """Check SC875 successful transaction response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check SC875 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3173", "API-3173")
@pytest.mark.skip(reason="SC875 87501 cannot currently be reproduced. Tracked under Test Automation Risk Management.")
@scenario("Check SC875 unsuccessful transaction response")
def test_sc875_unsuccessful_transaction_response():
    """Check SC875 unsuccessful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct payload for {conditions}"), target_fixture="payload")
def create_correct_payload(conditions):
    return sc875_payload_setup(conditions)


@given(parsers.parse("I create the payload with {conditions}"), target_fixture="payload")
def create_invalid_payload(conditions):
    return sc875_payload_setup(conditions)


@given("I send the request to the Azure SC875 endpoint", target_fixture="response_azure")
def send_azure_request(payload):
    endpoint = build_api_endpoint("SC875", system="AZURE")

    headers = {"Content-Type": "application/xml", "SOAPAction": "tns:inquire"}

    response = requests.post(endpoint, data=payload["request_body"].encode("utf-8"), headers=headers, timeout=30)

    return response.text, response.status_code


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I can see result code {result_code} returned"))
def validate_result_code(api_client, response_azure, result_code):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see result message "{result_message}" returned'))
def validate_result_message(api_client, response_azure, result_message):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.result_message, result_message)


@then(parsers.parse('I can see hasMedicalAppealDecision "{has_medical_appeal_decision}" returned'))
def validate_has_medical_appeal_decision(api_client, response_azure, has_medical_appeal_decision):
    api_client.check_value_in_xml_response(
        response_azure, dot_xml_pattern.has_medical_appeal_decision, has_medical_appeal_decision
    )
