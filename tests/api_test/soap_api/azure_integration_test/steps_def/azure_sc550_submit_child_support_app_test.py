from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

import apps.services.integration_soap.expected_responses.sc550_responses_azure as sc
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc550_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify azure SC550 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Verify azure SC550 successful response")
def test_azure_sc550_successful_response():
    """Verify azure SC550 successful response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify azure SC550 responses when the request details contain missing values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Verify azure SC550 responses when the request details contain missing values")
def test_azure_sc550_response_with_missing_values():
    """Verify azure SC550 responses when the request details contain missing values"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Verify azure SC550 responses when the request details contain invalid ird values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Verify azure SC550 responses when the request details contain invalid ird values")
def test_azure_sc550_response_with_invalid_ird_values():
    """Verify azure SC550 responses when the request details contain invalid ird values"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Verify azure SC550 responses when the request details contain invalid values
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2961", "User Story")
@scenario("Verify azure SC550 responses when the request details contain invalid values")
def test_azure_sc550_response_with_other_invalid_values():
    """Verify azure SC550 responses when the request details contain invalid values"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc550_payload_setup()


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return sc550_payload_setup(conditions=conditions)


@given("I send the child support request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC550", system="AZURE")
    return api_client.send_post_request(endpoint, headers=payload[0], payload=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I see the response status code matches the expected code {status_code}"))
def validate_response_status_code(api_client, response_azure, status_code):
    api_client.compare_status_code(status_code, str(response_azure[1]))


@then("I see the response body matches the expected response body")
def validate_error_response(api_client, response_azure):
    api_client.compare_error_strings(sc.error_400, response_azure, "SC550")
