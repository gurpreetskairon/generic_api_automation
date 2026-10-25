import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc892_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4249", "User Story")
@scenario("Compare SC892 successful responses between IIB and Azure")
def test_compare_sc892_successful_responses():
    """Compare SC892 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Unsuccessful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4249", "User Story")
@scenario("Compare SC892 unsuccessful responses between IIB and Azure")
def test_compare_sc892_unsuccessful_responses():
    """Compare SC892 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC892 api payload for {condition}"), target_fixture="payload")
def create_sc892_payload(condition):
    return sc892_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC892 request to IIB endpoint", target_fixture="response_iib")
def send_sc892_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC892", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC892 request to Azure endpoint", target_fixture="response_azure")
def send_sc892_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC892", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC892")
def compare_sc892_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC892", ignore_element_order=True)
