from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc826_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC826 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Compare SC826 successful response")
def test_compare_sc826_successful_response():
    """Compare SC826 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC826 responses with a secured client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Compare SC826 responses with a secured client")
def test_compare_sc826_response_with_secured_client():
    """Compare SC826 responses with a secured client"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC826 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Compare SC826 responses with invalid data")
def test_compare_sc826_response_with_invalid_data():
    """Compare SC826 responses with invalid data"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC826 responses with invalid user
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Compare SC826 responses with invalid user")
def test_compare_sc826_response_with_invalid_user():
    """Compare SC826 responses with invalid user"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Compare SC826 responses with results containing more than 50 entries
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Compare SC826 responses with results containing more than 50 entries")
def test_compare_sc826_response_with_more_than_50_entries():
    """Compare SC826 responses with results containing more than 50 entries"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct api payload {payload_type}"), target_fixture="payload")
def create_correct_payload(payload_type):
    iib_headers, iib_body = sc826_payload_setup(payload_type=payload_type)
    azure_headers, azure_body = sc826_payload_setup(payload_type=payload_type)
    payloads = {
        "iib_headers": iib_headers,
        "iib_body": iib_body,
        "azure_headers": azure_headers,
        "azure_body": azure_body,
    }
    return payloads


@given(
    parsers.parse("I create the correct api payload {payload_type} with different {conditions}"),
    target_fixture="payload"
)
def create_different_payload(payload_type, conditions):
    iib_headers, iib_body = sc826_payload_setup(payload_type=payload_type, conditions=conditions)
    azure_headers, azure_body = sc826_payload_setup(payload_type=payload_type, conditions=conditions)
    payloads = {
        "iib_headers": iib_headers,
        "iib_body": iib_body,
        "azure_headers": azure_headers,
        "azure_body": azure_body,
    }
    return payloads


@given("I send the request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC826", system="IIB")
    return api_client.send_post_request(endpoint, headers=payload["iib_headers"], payload=payload["iib_body"])


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC826", system="AZURE")
    return api_client.send_post_request(endpoint, headers=payload["azure_headers"], payload=payload["azure_body"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC826")
