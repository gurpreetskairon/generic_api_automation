from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc849_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


@pytest.mark.skip("The release date for this service has been delayed")
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare sc849 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Compare SC849 successful response")
def test_compare_sc849_successful_response():
    """Compare sc849 successful response"""


@pytest.mark.skip("The release date for this service has been delayed")
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare sc849 client not recognised response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Compare SC849 client not recognised response")
def test_compare_sc849_client_not_recognised_response():
    """Compare sc849 client not recognised response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return sc849_payload_setup(condition=conditions)


@given("I send the inquire provider request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC849", system="IIB")
    response = api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])
    return response


@given("I send the inquire provider request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC849", system="AZURE")
    response = api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])
    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC849")
