from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc246_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify SC246 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3058", "User Story")
@scenario("Verify SC246 successful response")
def test_compare_sc246_successful_response():
    """Verify SC246 successful response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify SC246 responses for client with no id verification
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3058", "User Story")
@scenario("Verify SC246 responses for client with no id verification")
def test_compare_sc246_response_for_client_with_no_verification():
    """Verify SC246 responses for client with no id verification"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Verify SC246 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Verify SC246 responses with invalid data")
def test_compare_sc246_response_with_invalid_data():
    """Verify SC246 responses with invalid data"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Verify SC246 responses with invalid header values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Verify SC246 responses with invalid header values")
def test_compare_sc246_response_with_invalid_header_values():
    """Verify SC246 responses with invalid header values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    tz = timezone(timedelta(hours=12))
    formatted_datetime = datetime.now(tz).isoformat(timespec="seconds")
    azure_headers, azure_body = sc246_payload_setup(date_time=formatted_datetime)
    dt = datetime.fromisoformat(formatted_datetime)
    azure_response_datetime = dt.strftime("%Y%m%dT%H%M%S")

    payloads = {
        "azure_headers": azure_headers,
        "azure_body": azure_body,
        "azure_response_datetime": azure_response_datetime,
        "condition": None,
    }
    return payloads


@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    tz = timezone(timedelta(hours=12))
    formatted_datetime = datetime.now(tz).isoformat(timespec="seconds")
    azure_headers, azure_body = sc246_payload_setup(conditions=conditions, date_time=formatted_datetime)
    dt = datetime.fromisoformat(formatted_datetime)
    azure_response_datetime = dt.strftime("%Y%m%dT%H%M%S")
    payloads = {
        "azure_headers": azure_headers,
        "azure_body": azure_body,
        "azure_response_datetime": azure_response_datetime,
        "condition": conditions,
    }
    return payloads


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC246", system="AZURE")
    return (
        payload["azure_response_datetime"],
        api_client.send_post_request(endpoint, payload=payload["azure_body"], headers=payload["azure_headers"]),
        payload["condition"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_azure):
    root = Path(__file__).resolve().parents[5]
    if response_azure[2] == "no_identity_verification":
        expected_response_filepath = list(root.rglob("sc246_no_id_verification_responses_azure.xml"))
        expected_response = expected_response_filepath[0].read_text(encoding="utf-8")
    else:
        expected_response_filepath = list(root.rglob("sc246_responses_azure.xml"))
        expected_response = expected_response_filepath[0].read_text(encoding="utf-8")

    updated_response = expected_response.replace("20260617T171055", response_azure[0])
    api_client.compare_soap_responses(
        updated_response, response_azure[1][0], "SC246", ignore_tags=["transactionId", "expiry"]
    )


@then(parsers.parse("I can see result code {result_code} is the same in both responses"))
def compare_result_code(api_client, response_azure, result_code):
    api_client.check_value_in_xml_response(response_azure[1], dot_xml_pattern.result_code, result_code)


@then(parsers.parse("I can see result message {result_message} is the same in both responses"))
def compare_result_message(api_client, response_azure, result_message):
    api_client.check_value_in_xml_response(response_azure[1], dot_xml_pattern.status_message, result_message)
