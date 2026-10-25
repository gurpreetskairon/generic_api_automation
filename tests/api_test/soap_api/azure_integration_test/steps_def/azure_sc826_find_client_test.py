from pathlib import Path
from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc826_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify SC826 successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Verify SC826 successful responses")
def test_verify_sc826_successful_responses():
    """Verify SC826 successful responses"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify SC826 responses with a secured client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Verify SC826 responses with a secured client")
def test_verify_sc826_response_with_secured_client():
    """Verify SC826 responses with a secured client"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Verify SC826 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Verify SC826 responses with invalid data")
def test_verify_sc826_response_with_invalid_data():
    """Verify SC826 responses with invalid data"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Verify SC826 responses with invalid user
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Verify SC826 responses with invalid user")
def test_verify_sc826_response_with_invalid_user():
    """Verify SC826 responses with invalid user"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Verify SC826 responses with results containing more than 50 entries
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Verify SC826 responses with results containing more than 50 entries")
def test_verify_sc826_response_with_more_than_50_entries():
    """Verify SC826 responses with results containing more than 50 entries"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct api payload {payload_type}"), target_fixture="payload")
def create_correct_payload(payload_type):
    azure_headers, azure_body = sc826_payload_setup(payload_type=payload_type)
    payloads = {"azure_headers": azure_headers, "azure_body": azure_body}
    return payloads


@given(
    parsers.parse("I create the correct api payload {payload_type} with different {conditions}"),
    target_fixture="payload"
)
def create_different_payload(payload_type, conditions):
    azure_headers, azure_body = sc826_payload_setup(payload_type=payload_type, conditions=conditions)
    payloads = {"azure_headers": azure_headers, "azure_body": azure_body}
    return payloads


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC826", system="AZURE")
    return api_client.send_post_request(endpoint, headers=payload["azure_headers"], payload=payload["azure_body"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I can see the responses are identical for payload {payload_type}"))
def validate_response(api_client, response_azure, payload_type):
    root = Path(__file__).resolve().parents[5]
    if payload_type == "all_but_ird":
        expected_response_filepath = list(root.rglob("sc826_all_criteria_except_ird_response.xml"))
    elif payload_type == "dob_only":
        expected_response_filepath = list(root.rglob("sc826_dob_response.xml"))
    elif payload_type == "full_name":
        expected_response_filepath = list(root.rglob("sc826_full_name_response.xml"))
    elif payload_type == "ird_only":
        expected_response_filepath = list(root.rglob("sc826_ird_only_response.xml"))
    elif payload_type == "name_gender":
        expected_response_filepath = list(root.rglob("sc826_name_and_gender_response.xml"))
    else:
        raise Exception(f"Invalid payload type: {payload_type}")

    expected_response = expected_response_filepath[0].read_text(encoding="utf-8")
    api_client.compare_soap_responses(
        expected_response, response_azure[0], "SC862", ignore_tags=["auditId", "requestDateTime", "transactionId"]
    )


@then(parsers.parse("I can see result code {result_code} is the same in both responses"))
def compare_result_code(api_client, response_azure, result_code):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.result_code, result_code)


@then(parsers.parse("I can see subresult message {subresult_message} is the same in both responses"))
def compare_subresult_message(api_client, response_azure, subresult_message):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.subresult_message, subresult_message)


@then(parsers.parse("I can see subresult code {subresult_code} is the same in both responses"))
def compare_subresult_code(api_client, response_azure, subresult_code):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.subresult_code, subresult_code)


@then(parsers.parse("I can see result message {result_message} is the same in both responses"))
def compare_result_message(api_client, response_azure, result_message):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.status_message, result_message)
