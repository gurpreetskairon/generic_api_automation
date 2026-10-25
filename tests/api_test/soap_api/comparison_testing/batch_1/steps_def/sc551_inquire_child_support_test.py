from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc551_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC551 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2990", "User Story")
@scenario("Compare SC551 successful response")
def test_compare_sc551_successful_response():
    """Compare SC551 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC551 responses when the request details contain invalid values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2990", "User Story")
@scenario("Compare SC551 responses when the request details contain invalid values")
def test_compare_sc551_response_with_missing_values():
    """Compare SC551 responses when the request details contain invalid values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload(formatted_datetime):
    return sc551_payload_setup(ird_num="139628047", client_id="021215905", date_time=formatted_datetime)


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions, formatted_datetime):
    return sc551_payload_setup(
        ird_num="139628047", client_id="021215905", conditions=conditions, date_time=formatted_datetime
    )


@given("I send the child support request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC551", system="IIB")
    return api_client.send_post_request(endpoint, headers=payload[0], payload=payload[1])


@given("I send the child support request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC551", system="AZURE")
    return api_client.send_post_request(endpoint, headers=payload[0], payload=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC551")
