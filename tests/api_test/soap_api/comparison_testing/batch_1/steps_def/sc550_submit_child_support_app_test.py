from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc550_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC550 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Compare SC550 successful response")
def test_compare_sc550_successful_response():
    """Compare SC550 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC550 responses when the request details contain missing values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Compare SC550 responses when the request details contain missing values")
def test_compare_sc550_response_with_missing_values():
    """Compare SC550 responses when the request details are missing values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC550 responses when the request details contain invalid ird values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Compare SC550 responses when the request details contain invalid ird values")
def test_compare_sc550_response_with_invalid_ird_values():
    """Compare SC550 responses when the request details contain invalid values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC550 responses when the request details contain invalid values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Compare SC550 responses when the request details contain invalid values")
def test_compare_sc550_response_with_other_invalid_values():
    """Compare SC550 responses when the request details contain invalid values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    iib_payload = sc550_payload_setup()
    azure_payload = sc550_payload_setup()
    return iib_payload, azure_payload


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    iib_payload = sc550_payload_setup(conditions=conditions)
    azure_payload = sc550_payload_setup(conditions=conditions)
    return iib_payload, azure_payload


@given("I send the child support request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC550", system="IIB")
    return api_client.send_post_request(endpoint, headers=payload[0][0], payload=payload[0][1])


@given("I send the child support request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC550", system="AZURE")
    return api_client.send_post_request(endpoint, headers=payload[1][0], payload=payload[1][1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the error responses are identical")
def validate_error_response(api_client, response_iib, response_azure):
    api_client.compare_error_strings(response_iib[0], response_azure[0], "SC550")


@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "SC550")
