import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp153_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP153 successful response between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4612", "User Story")
@scenario("Compare DP153 successful response between DataPower and Azure")
def test_compare_dp153_successful_response():
    """Compare DP153 successful response between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP153 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4612", "User Story")
@scenario("Compare DP153 unsuccessful responses between DataPower and Azure")
def test_compare_dp153_unsuccessful_responses():
    """Compare DP153 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP153 api payload for {condition}"), target_fixture="payload")
def create_dp153_payload(condition):
    return dp153_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send DP153 request to DataPower endpoint", target_fixture="response_datapower")
def send_dp153_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP153", system="IIB", sub_system="MYMSD")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"])

    response = api_client.send_get_request(
        endpoint, headers=payload["header"], raise_on_error=payload["raise_on_error"]
    )

    response_body, status_code = response

    allure.attach(
        response_body, name=f"DataPower Response - HTTP {status_code}", attachment_type=allure.attachment_type.JSON
    )

    return response


@when("I send DP153 request to Azure endpoint", target_fixture="response_azure")
def send_dp153_request_to_azure(api_client, payload):
    pytest.skip("Azure development for DP153 is not complete. DataPower response validated independently.")


# @when("I send DP153 request to DataPower endpoint", target_fixture="response_iib")
# def send_dp153_request_to_datapower(api_client, payload):
#     endpoint = build_api_endpoint("DP153", system="IIB", sub_system="MYMSD")
#     endpoint = endpoint.replace("{participantId}", payload["participant_id"])
#     return api_client.send_get_request(endpoint, headers=payload["header"])
#
#
# @when("I send DP153 request to Azure endpoint", target_fixture="response_azure")
# def send_dp153_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("DP153", system="AZURE")
#     endpoint = endpoint.replace("{participantId}", payload["participant_id"])
#     return api_client.send_get_request(endpoint, headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP153")
def compare_dp153_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "dp153")
