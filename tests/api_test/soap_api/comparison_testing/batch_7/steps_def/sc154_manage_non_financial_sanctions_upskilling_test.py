import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc154_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC154 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4613", "User Story")
@scenario("Compare SC154 successful responses between IIB and Azure")
def test_compare_sc154_successful_responses():
    """Compare SC154 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC154 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4613", "User Story")
@scenario("Compare SC154 unsuccessful responses between IIB and Azure")
def test_compare_sc154_unsuccessful_responses():
    """Compare SC154 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC154 api payload for {condition}"), target_fixture="payload")
def create_sc154_payload(condition):
    return sc154_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC154 request to IIB endpoint", target_fixture="response_iib")
def send_sc154_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC154", system="IIB")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"]).replace("{upskillingId}", payload["upskilling_id"])
    response = api_client.send_rest_put_request(endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False)
    response_body, status_code = response
    allure.attach(response_body, name=f"IIB Response - HTTP {status_code}", attachment_type=allure.attachment_type.JSON)
    return response


@when("I send SC154 request to Azure endpoint", target_fixture="response_azure")
def send_sc154_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC154", system="AZURE")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"]).replace("{upskillingId}", payload["upskilling_id"])
    response = api_client.send_rest_put_request(endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False)
    response_body, status_code = response
    allure.attach(response_body, name=f"Azure Response - HTTP {status_code}", attachment_type=allure.attachment_type.JSON)
    return response

# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC154")
def compare_sc154_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "SC154")
