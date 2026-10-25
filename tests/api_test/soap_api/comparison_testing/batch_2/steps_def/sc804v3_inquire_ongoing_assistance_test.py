from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc804_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC804 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Compare SC804v3 successful response")
def test_compare_sc804v3_successful_response():
    """Compare SC804v3 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC804 client not recognised response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Compare SC804v3 client not recognised response")
def test_compare_sc804v3_client_not_recognised_response():
    """Compare SC804v3 client not recognised response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct api payload with {client_type}"), target_fixture="payload")
def create_correct_payload(client_type):
    return sc804_payload_setup(payload_type="v3", client_type=client_type)


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return sc804_payload_setup(payload_type="v3", condition=conditions)


@given("I send the inquire provider request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC804v3", system="IIB")
    response = api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])
    return response


@given("I send the inquire provider request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC804v3", system="AZURE")
    response = api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])
    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC804v3", ignore_element_order=True)
