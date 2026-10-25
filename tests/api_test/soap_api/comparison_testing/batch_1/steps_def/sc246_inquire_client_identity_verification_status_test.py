from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc246_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC246 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3058", "User Story")
@scenario("Compare SC246 successful response")
def test_compare_sc246_successful_response():
    """Compare SC246 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC246 responses for client with no id verification
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3058", "User Story")
@scenario("Compare SC246 responses for client with no id verification")
def test_compare_sc246_response_for_client_with_no_verification():
    """Compare SC246 responses for client with no id verification"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC246 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Compare SC246 responses with invalid data")
def test_compare_sc246_response_with_invalid_data():
    """Compare SC246 responses with invalid data"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC246 responses with invalid header values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3062", "User Story")
@scenario("Compare SC246 responses with invalid header values")
def test_compare_sc246_response_with_invalid_header_values():
    """Compare SC246 responses with invalid header values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload(formatted_datetime):
    iib_headers, iib_body = sc246_payload_setup(date_time=formatted_datetime)
    azure_headers, azure_body = sc246_payload_setup(date_time=formatted_datetime)
    payloads = {
        "iib_headers": iib_headers,
        "iib_body": iib_body,
        "azure_headers": azure_headers,
        "azure_body": azure_body,
    }
    return payloads


@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions, formatted_datetime):
    iib_headers, iib_body = sc246_payload_setup(conditions=conditions, date_time=formatted_datetime)
    azure_headers, azure_body = sc246_payload_setup(conditions=conditions, date_time=formatted_datetime)
    payloads = {
        "iib_headers": iib_headers,
        "iib_body": iib_body,
        "azure_headers": azure_headers,
        "azure_body": azure_body,
    }
    return payloads


@given("I send the request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC246", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["iib_body"], headers=payload["iib_headers"])


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC246", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["azure_body"], headers=payload["azure_headers"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC246")
