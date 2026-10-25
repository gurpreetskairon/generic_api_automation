import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc817_payload_setup
from utils.bdd_utils.scenario import scenario


# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC817 successful client provisioning responses
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4306", "User Story")
# @scenario("Compare SC817 successful client provisioning responses between IIB and Azure")
# def test_compare_sc817_successful_client_provisioning_responses():
#     """Compare SC817 successful client provisioning responses between IIB and Azure"""
#
#
# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC817 successful provider provisioning responses
# ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4306", "User Story")
# @scenario("Compare SC817 successful provider provisioning responses between IIB and Azure")
# def test_compare_sc817_successful_provider_provisioning_responses():
#     """Compare SC817 successful provider provisioning responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC817 unsuccessful authentication responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4306", "User Story")
@scenario("Compare SC817 unsuccessful authentication responses between IIB and Azure")
def test_compare_sc817_unsuccessful_authentication_responses():
    """Compare SC817 unsuccessful authentication responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC817 api payload for {condition}"), target_fixture="payload")
def create_sc817_payload(condition):
    return sc817_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC817 request to IIB endpoint", target_fixture="response_iib")
def send_sc817_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC817", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC817 request to Azure endpoint", target_fixture="response_azure")
def send_sc817_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC817", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC817")
def compare_sc817_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC817", ignore_element_order=True)
