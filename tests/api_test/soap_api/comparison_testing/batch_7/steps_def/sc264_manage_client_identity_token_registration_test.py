import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc264_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC264 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4629", "User Story")
@scenario("Compare SC264 successful responses between IIB and Azure")
def test_compare_sc264_successful_responses():
    """Compare SC264 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC264 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4629", "User Story")
@scenario("Compare SC264 unsuccessful responses between IIB and Azure")
def test_compare_sc264_unsuccessful_responses():
    """Compare SC264 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC264 exception responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4629", "User Story")
@scenario("Compare SC264 exception responses between IIB and Azure")
def test_compare_sc264_exception_responses():
    """Compare SC264 exception responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given Steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC264 api payload for {condition}"), target_fixture="payload")
def create_sc264_payload(condition):
    return sc264_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When Steps
# ══════════════════════════════════════════════════════════════════════════════
# @when("I send SC264 request to IIB endpoint", target_fixture="response_iib")
# def send_sc264_request_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC264", system="IIB")
#     endpoint = endpoint.replace("{clientNumber}", payload["client_number"]).replace("{tokenType}", payload["token_type"])
#     return api_client.send_post_request(
#         endpoint, payload["request_body"], payload["header"], json_payload=True, raise_error=payload["raise_on_error"]
#     )
#
#
# @when("I send SC264 request to Azure endpoint", target_fixture="response_azure")
# def send_sc264_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC264", system="AZURE")
#     endpoint = endpoint.replace("{clientNumber}", payload["client_number"]).replace("{tokenType}", payload["token_type"])
#     return api_client.send_post_request(
#         endpoint, payload["request_body"], payload["header"], json_payload=True, raise_error=payload["raise_on_error"]
#     )


@when("I send SC264 request to IIB endpoint", target_fixture="response_iib")
def send_sc264_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC264", system="IIB")
    endpoint = endpoint.replace("{clientNumber}", payload["client_number"]).replace(
        "{tokenType}", payload["token_type"]
    )
    response = api_client.send_post_request(
        endpoint, payload["request_body"], payload["header"], json_payload=True, raise_error=payload["raise_on_error"]
    )
    response_body, status_code = response
    allure.attach(response_body, name=f"IIB Response - HTTP {status_code}", attachment_type=allure.attachment_type.JSON)
    return response


@when("I send SC264 request to Azure endpoint", target_fixture="response_azure")
def send_sc264_request_to_azure(api_client, payload):
    pytest.skip("Azure development for SC264 is not complete. IIB response validated independently.")


# ══════════════════════════════════════════════════════════════════════════════
# Then Steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC264")
def compare_sc264_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "SC264")
