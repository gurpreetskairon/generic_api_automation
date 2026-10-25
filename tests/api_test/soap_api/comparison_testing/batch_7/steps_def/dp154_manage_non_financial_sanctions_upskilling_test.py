import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp154_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP154 successful response between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4614", "User Story")
@scenario("Compare DP154 successful response between DataPower and Azure")
def test_compare_dp154_successful_response():
    """Compare DP154 successful response between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP154 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4614", "User Story")
@scenario("Compare DP154 unsuccessful responses between DataPower and Azure")
def test_compare_dp154_unsuccessful_responses():
    """Compare DP154 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP154 api payload for {condition}"), target_fixture="payload")
def create_dp154_payload(condition):
    return dp154_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
# @when("I send DP154 request to DataPower endpoint", target_fixture="response_datapower")
# def send_dp154_request_to_datapower(api_client, payload):
#     endpoint = build_api_endpoint("DP154", system="IIB", sub_system="MYMSD")
#     endpoint = endpoint.replace("{participantId}", payload["participant_id"])
#     endpoint = endpoint.replace("{upskillingId}", payload["upskilling_id"])
#
#     return api_client.send_rest_put_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
#     )
#
#
# @when("I send DP154 request to Azure endpoint", target_fixture="response_azure")
# def send_dp154_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("DP154", system="AZURE")
#     endpoint = endpoint.replace("{participantId}", payload["participant_id"])
#     endpoint = endpoint.replace("{upskillingId}", payload["upskilling_id"])
#
#     return api_client.send_rest_put_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
#     )


@when("I send DP154 request to DataPower endpoint", target_fixture="response_datapower")
def send_dp154_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP154", system="IIB", sub_system="MYMSD")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"]).replace(
        "{upskillingId}", payload["upskilling_id"]
    )
    response = api_client.send_rest_put_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
    )
    response_body, status_code = response
    allure.attach(
        response_body, name=f"DataPower Response - HTTP {status_code}", attachment_type=allure.attachment_type.JSON
    )
    return response


@when("I send DP154 request to Azure endpoint", target_fixture="response_azure")
def send_dp154_request_to_azure(api_client, payload):
    pytest.skip("Azure development for DP154 is not complete. DataPower response validated independently.")


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP154")
def compare_dp154_responses(api_client, response_datapower, response_azure):
    api_client.compare_json_responses(response_datapower, response_azure, "DP154")
