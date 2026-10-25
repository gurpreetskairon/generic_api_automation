import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc540_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC540 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3989", "API-3989")
@scenario("Compare SC540 successful responses between IIB and Azure")
def test_compare_sc540_successful_responses():
    """Compare SC540 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC540 unuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3989", "API-3989")
@scenario("Compare SC540 unsuccessful responses between IIB and Azure")
def test_compare_sc540_unsuccessful_responses():
    """Compare SC540 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC540 api payload for {condition}"), target_fixture="payload")
def create_sc540_payload(condition):
    return sc540_payload_setup(condition=condition)


@when("I send SC540 request to IIB endpoint", target_fixture="response_iib")
def send_sc540_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC540", system="IIB")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC540 request to Azure endpoint", target_fixture="response_azure")
def send_sc540_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC540", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC540")
def compare_sc540_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC540", ignore_element_order=True)
