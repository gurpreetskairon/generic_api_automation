import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc820_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC820 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3917", "User Story")
@scenario("Compare SC820 successful responses between IIB and Azure")
def test_compare_sc820_successful_responses():
    """Compare SC820 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC820 api payload for {condition}"), target_fixture="payload")
def create_sc820_payload(condition):
    return sc820_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC820 request to IIB endpoint", target_fixture="response_iib")
def send_sc820_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC820", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@when("I send SC820 request to Azure endpoint", target_fixture="response_azure")
def send_sc820_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC820", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC820")
def compare_sc820_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC820", ignore_element_order=True,
                                      ignore_tags=["decisionId"])
