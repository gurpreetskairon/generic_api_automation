import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc897_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC897 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4302", "User Story")
@scenario("Compare SC897 successful responses between IIB and Azure")
def test_compare_sc897_successful_responses():
    """Compare SC897 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC897 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4302", "User Story")
@scenario("Compare SC897 unsuccessful responses between IIB and Azure")
def test_compare_sc897_unsuccessful_responses():
    """Compare SC897 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC897 api payload for {condition}"), target_fixture="payload")
def create_sc897_payload(condition):
    return sc897_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC897 request to IIB endpoint", target_fixture="response_iib")
def send_sc897_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC897", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC897 request to Azure endpoint", target_fixture="response_azure")
def send_sc897_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC897", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC897")
def compare_sc897_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC897", ignore_element_order=True)
