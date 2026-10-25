import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc861_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC861 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4138", "User Story")
@scenario("Compare SC861 successful responses between IIB and Azure")
def test_compare_sc861_successful_responses():
    """Compare SC861 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC861 successful responses between IIB and Azure with an invalid swn
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4138", "User Story")
@scenario("Compare SC861 successful responses between IIB and Azure with an invalid swn")
def test_compare_sc861_successful_responses_with_invalid_swn():
    """Compare SC861 successful responses between IIB and Azure with an invalid swn"""


@given(parsers.parse("I create the SC861 api payload for {condition}"), target_fixture="payload")
def create_sc861_payload(condition):
    return sc861_payload_setup(condition=condition)


@when("I send SC861 request to IIB endpoint", target_fixture="response_iib")
def send_sc861_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC861", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@when("I send SC861 request to Azure endpoint", target_fixture="response_azure")
def send_sc861_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC861", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@then("I can see all the responses are identical for SC861")
def compare_sc861_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC861", ignore_element_order=True)
