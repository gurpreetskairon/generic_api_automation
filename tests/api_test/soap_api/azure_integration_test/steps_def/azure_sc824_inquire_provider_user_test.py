from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc824_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify SC824 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Verify SC824 successful response")
def test_compare_sc824_successful_response():
    """Verify SC824 successful response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify SC824 client not recognised response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Verify SC824 client not recognised response")
def test_compare_sc824_client_not_recognised_response():
    """Verify SC824 client not recognised response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc824_payload_setup()


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return sc824_payload_setup(conditions)


@given("I send the inquire provider request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC824", system="AZURE")
    response = api_client.send_post_request(endpoint, payload=payload[0], headers={"Content-Type": "application/xml"})
    return response, payload[1]


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I can see the result code {result_code} is the same in both responses"))
def compare_result_code(api_client, response_azure, result_code):
    api_client.check_value_in_xml_response(response_azure[0], dot_xml_pattern.result_code, result_code)


@then(parsers.parse("I can see the result message {result_message} is the same in both responses"))
def compare_result_message(api_client, response_azure, result_message):
    api_client.check_value_in_xml_response(response_azure[0], dot_xml_pattern.status_message, result_message)


@then(parsers.parse("I can see the email address in the response matches"))
def compare_contact_details_value(api_client, response_azure):
    api_client.check_value_in_xml_response(response_azure[0], dot_xml_pattern.inq_provider,
                                           "gabriela@dwell.org.nz")
