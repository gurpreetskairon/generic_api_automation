import allure
from pytest_bdd import given, parsers, then, when
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc556_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC556 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3774", "User Story")
@scenario("Compare SC556 successful responses between IIB and Azure")
def test_compare_sc556_successful_responses():
    """Compare SC556 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC556 negative transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3774", "User Story")
@scenario("Compare SC556 negative responses between IIB and Azure")
def test_compare_sc556_negative_responses():
    """Compare SC556 negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC556 api payload for {condition}"), target_fixture="payload")
def create_sc556_payload(condition):
    return sc556_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC556 request to IIB endpoint", target_fixture="response_iib")
def send_sc556_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC556", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@when("I send SC556 request to Azure endpoint", target_fixture="response_azure")
def send_sc556_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC556", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC556")
def compare_sc556_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC556", ignore_element_order=True)
