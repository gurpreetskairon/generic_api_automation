import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc821_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC821 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4271", "User Story")
@scenario("Compare SC821 successful responses between IIB and Azure")
def test_compare_sc821_successful_responses():
    """Compare SC821 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC821 api payload for {condition}"), target_fixture="payload")
def create_sc821_payload(condition):
    return sc821_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC821 request to IIB endpoint", target_fixture="response_iib")
def send_sc821_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC821", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@when("I send SC821 request to Azure endpoint", target_fixture="response_azure")
def send_sc821_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC821", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC821")
def compare_sc821_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC821", ignore_element_order=True)
