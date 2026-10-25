from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc899_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC899 successful responses between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3178", "API-3178")
@scenario("Compare SC899 successful responses between Azure and IIB")
def test_compare_sc899_successful_responses_between_azure_and_iib():
    """Compare SC899 successful responses between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC899 successful responses between Azure and IIB with conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3178", "API-3178")
@scenario("Compare SC899 successful responses between Azure and IIB with conditions")
def test_compare_sc899_successful_responses_between_azure_and_iib_with_conditions():
    """Compare SC899 successful responses between Azure and IIB with conditions"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I created the correct SC899 api payload"), target_fixture="payload")
def create_correct_sc899_payload():
    return sc899_payload_setup()


@given(parsers.parse("I create the correct SC899 api payload with {conditions}"), target_fixture="payload")
def create_sc899_payload_for_positive_condition(conditions):
    return sc899_payload_setup(conditions)


@given("I send the request to the IIB endpoint", target_fixture="iib_response")
def send_inquire_participant_request_for_client_tags_and_flags_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC899", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[0], headers=payload[1])


@given("I send the request to the Azure endpoint", target_fixture="azure_response")
def send_inquire_participant_request_for_client_tags_and_flags_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC899", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[0], headers=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, iib_response, azure_response):
    api_client.compare_soap_responses(iib_response[0], azure_response[0], "SC899", ignore_tags=["incomeID", "incomeID"])
