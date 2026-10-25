from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc551_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify SC551 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2990", "User Story")
@scenario("Verify SC551 successful response")
def test_compare_sc551_successful_response():
    """Verify SC551 successful response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify SC551 responses when the request details contain invalid values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2990", "User Story")
@scenario("Verify SC551 responses when the request details contain invalid values")
def test_compare_sc551_response_with_missing_values():
    """Verify SC551 responses when the request details contain invalid values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    payload_setup = sc551_payload_setup(ird_num="139628047", client_id="021215905")
    payloads = {"iib": payload_setup, "azure": payload_setup}
    return payloads


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    azure_payload = sc551_payload_setup(ird_num="139628047", client_id="021215905", conditions=conditions)
    payloads = {"azure": azure_payload}
    return payloads


@given("I send the child support request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC551", system="AZURE")
    return api_client.send_post_request(endpoint, headers=payload["azure"][0], payload=payload["azure"][1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_responses_xml(response_iib[0], response_azure[0], "SC551")


@then(parsers.parse("I can see result code {result_code} is the same in both responses"))
def compare_result_code(api_client, response_azure, result_code):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern, result_code)


@then(parsers.parse("I can see subresult message {subresult_message} is the same in both responses"))
def compare_subresult_message(api_client, response_azure, subresult_message):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.status_message, subresult_message)
