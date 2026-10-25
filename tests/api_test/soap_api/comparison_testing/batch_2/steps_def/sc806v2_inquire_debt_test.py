import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc806v2_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC806 successful response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3465", "User Story")
@scenario("Compare SC806v2 successful response")
def test_compare_sc806v2_successful_response():
    """Compare the successful SC806v2 response returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC806v2 no matching record response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3465", "User Story")
@scenario("Compare SC806v2 no matching record response")
def test_compare_sc806v2_no_matching_record_response():
    """Compare the SC806v2 no-matching-record response returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given("I create the correct SC806v2 api payload", target_fixture="payload")
def create_correct_sc806v2_payload():
    return sc806v2_payload_setup()


@given(parsers.parse("I create the SC806v2 api payload for {condition}"), target_fixture="payload")
def create_sc806v2_payload_for_condition(condition):
    return sc806v2_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC806v2 inquire debt request to IIB endpoint", target_fixture="response_iib")
def send_sc806v2_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC806", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC806v2 inquire debt request to Azure endpoint", target_fixture="response_azure")
def send_sc806v2_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC806", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC806v2")
def compare_sc806v2_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC806v2", ignore_element_order=True)
