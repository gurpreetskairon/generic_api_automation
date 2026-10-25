import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc879_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC879 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4248", "User Story")
@scenario("Compare SC879 successful responses between IIB and Azure")
def test_compare_sc879_successful_responses():
    """Compare SC879 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC879 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4248", "User Story")
@scenario("Compare SC879 unsuccessful responses between IIB and Azure")
def test_compare_sc879_unsuccessful_responses():
    """Compare SC879 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC879 api payload for {condition}"), target_fixture="payload")
def create_sc879_payload(condition):
    return sc879_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC879 request to IIB endpoint", target_fixture="response_iib")
def send_sc879_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC879", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC879 request to Azure endpoint", target_fixture="response_azure")
def send_sc879_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC879", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC879")
def compare_sc879_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC879", ignore_element_order=True)
