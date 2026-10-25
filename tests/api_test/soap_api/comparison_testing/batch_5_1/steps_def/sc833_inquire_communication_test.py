import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc833_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC833 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4136", "User Story")
@scenario("Compare SC833 successful responses between IIB and Azure")
def test_compare_sc833_successful_responses():
    """Compare SC833 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC833 api payload for {condition}"), target_fixture="payload")
def create_sc833_payload(condition):
    return sc833_payload_setup(condition=condition)


@when("I send SC833 request to IIB endpoint", target_fixture="response_iib")
def send_sc833_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC833", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@when("I send SC833 request to Azure endpoint", target_fixture="response_azure")
def send_sc833_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC833", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC833")
def compare_sc833_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC833", ignore_element_order=True)
