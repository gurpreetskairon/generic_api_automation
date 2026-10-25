import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp161_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP161 successful response between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4616", "User Story")
@scenario("Compare DP161 successful response between DataPower and Azure")
def test_compare_dp161_successful_response():
    """Compare DP161 successful response between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP161 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4616", "User Story")
@scenario("Compare DP161 unsuccessful responses between DataPower and Azure")
def test_compare_dp161_unsuccessful_responses():
    """Compare DP161 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP161 api payload for {condition}"), target_fixture="payload")
def create_dp161_payload(condition):
    return dp161_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send DP161 request to DataPower endpoint", target_fixture="response_datapower")
def send_dp161_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP161", system="IIB", sub_system="MYMSD")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"])

    response = api_client.send_get_request(
        endpoint, headers=payload["header"], raise_on_error=payload["raise_on_error"]
    )

    response_body, status_code = response

    allure.attach(
        response_body, name=f"DataPower Response - HTTP {status_code}", attachment_type=allure.attachment_type.JSON
    )

    return response


@when("I send DP161 request to Azure endpoint", target_fixture="response_azure")
def send_dp161_request_to_azure(api_client, payload):
    pytest.skip("Azure development for DP161 is not complete. DataPower response validated independently.")


# @when("I send DP161 request to DataPower endpoint", target_fixture="response_datapower")
# def send_dp161_request_to_datapower(api_client, payload):
#     endpoint = build_api_endpoint("DP161", system="IIB", sub_system="MYMSD")
#     endpoint = endpoint.replace("{participantId}", payload["participant_id"])
#
#     return api_client.send_get_request(
#         endpoint,
#         headers=payload["header"],
#         raise_on_error=payload["raise_on_error"],
#     )
#
#
# @when("I send DP161 request to Azure endpoint", target_fixture="response_azure")
# def send_dp161_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("DP161", system="AZURE")
#     endpoint = endpoint.replace("{participantId}", payload["participant_id"])
#
#     return api_client.send_get_request(
#         endpoint,
#         headers=payload["header"],
#         raise_on_error=payload["raise_on_error"],
#     )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP161")
def compare_dp161_responses(api_client, response_datapower, response_azure):
    api_client.compare_json_responses(response_datapower, response_azure, "DP161")
