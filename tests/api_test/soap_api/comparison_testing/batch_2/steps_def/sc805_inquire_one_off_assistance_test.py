import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc805_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC805 successful response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3459", "User Story")
@scenario("Compare SC805 successful response")
def test_compare_sc805_successful_response():
    """Compare the successful SC805 response returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC805 no matching record response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3459", "User Story")
@scenario("Compare SC805 no matching record response")
def test_compare_sc805_no_matching_record_response():
    """Compare the SC805 no-matching-record response returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given("I create the correct SC805 api payload", target_fixture="payload")
def create_correct_sc805_payload():
    return sc805_payload_setup()


@given(parsers.parse("I create the SC805 api payload for {condition}"), target_fixture="payload")
def create_sc805_payload_for_condition(condition):
    return sc805_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC805 inquire assistance request to IIB endpoint", target_fixture="response_iib")
def send_sc805_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC805", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC805 inquire assistance request to Azure endpoint", target_fixture="response_azure")
def send_sc805_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC805", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC805")
def compare_sc805_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC805", ignore_element_order=True)
