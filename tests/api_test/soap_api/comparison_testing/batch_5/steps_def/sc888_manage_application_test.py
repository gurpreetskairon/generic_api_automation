import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc888_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC888 successful responses for ID verification
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3900", "User Story")
@scenario("Compare SC888 successful responses between IIB and Azure for id verification")
def test_compare_sc888_successful_responses_id_verification():
    """Compare SC888 successful responses between IIB and Azure for id verification"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC888 successful responses for obligation verification
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3900", "User Story")
@scenario("Compare SC888 successful responses between IIB and Azure for obligation verification")
def test_compare_sc888_successful_responses_obligations_verification():
    """Compare SC888 successful responses between IIB and Azure for obligation verification"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC888 successful responses for negative scenarios
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3900", "User Story")
@scenario("Compare SC888 successful responses between IIB and Azure for negative scenarios")
def test_compare_sc888_successful_responses_negative_scenarios():
    """Compare SC888 successful responses between IIB and Azure for negative scenarios"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC888 api {payload_type} for {condition}"), target_fixture="payload")
def create_sc888_payload(payload_type, condition):
    return sc888_payload_setup(payload_type=payload_type, condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC888 request to IIB endpoint", target_fixture="response_iib")
def send_sc888_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC888", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@when("I send SC888 request to Azure endpoint", target_fixture="response_azure")
def send_sc888_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC888", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC888")
def compare_sc888_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC888", ignore_element_order=True)
