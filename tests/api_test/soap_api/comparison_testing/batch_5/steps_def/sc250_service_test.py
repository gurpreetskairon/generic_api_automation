import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc250_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC250 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4273", "User Story")
@scenario("Compare SC250 successful responses between IIB and Azure")
def test_compare_sc250_successful_responses():
    """Compare SC250 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the SC250 api payload", target_fixture="payload")
def create_sc250_payload():
    return sc250_payload_setup()


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC250 request to IIB endpoint", target_fixture="response_iib")
def send_sc250_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC250", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[0], headers=payload[1])


@when("I send SC250 request to Azure endpoint", target_fixture="response_azure")
def send_sc250_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC250", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[0], headers=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC250")
def compare_sc250_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC250", ignore_element_order=True)
