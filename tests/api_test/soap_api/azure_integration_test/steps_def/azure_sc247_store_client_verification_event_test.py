from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc247_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify SC247 successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Verify SC247 successful responses")
def test_compare_sc247_successful_response():
    """Verify SC247 successful responses"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify SC247 responses for no matching clients
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Verify SC247 responses for no matching clients")
def test_compare_sc247_response_for_no_matching_clients():
    """Verify SC247 responses for no matching clients"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Verify SC247 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Verify SC247 responses with invalid data")
def test_compare_sc247_response_with_invalid_data():
    """Verify SC247 responses with invalid data"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Verify SC247 responses with an invalid client number
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3308", "API-3308")
@scenario("Verify SC247 responses with an invalid client number")
def test_compare_sc247_response_with_invalid_client_number():
    """Verify SC247 responses with an invalid client number"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc247_payload_setup()


@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return sc247_payload_setup(conditions=conditions)


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC247", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[0], headers=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I can see result code {result_code} is the same in both responses"))
def compare_result_code(api_client, response_azure, result_code):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.result_code, result_code)


@then(parsers.parse("I can see result message {result_message} is the same in both responses"))
def compare_result_message(api_client, response_azure, result_message):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.status_message, result_message)


@then(parsers.parse("I can see subresult message {subresult_msg} is the same in both responses"))
def compare_subresult_message(api_client, response_azure, subresult_msg):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.subresult_message, subresult_msg)


@then(parsers.parse("I can see subresult code {subresult_code} is the same in both responses"))
def compare_subresult_code(api_client, response_azure, subresult_code):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.subresult_code, subresult_code)
