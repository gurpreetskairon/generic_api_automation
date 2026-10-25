import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc153_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC153 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4611", "User Story")
@scenario("Compare SC153 successful responses between IIB and Azure")
def test_compare_sc153_successful_responses():
    """Compare SC153 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC153 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4611", "User Story")
@scenario("Compare SC153 unsuccessful responses between IIB and Azure")
def test_compare_sc153_unsuccessful_responses():
    """Compare SC153 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC153 api payload for {condition}"), target_fixture="payload")
def create_sc153_payload(condition):
    return sc153_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC153 request to IIB endpoint", target_fixture="response_iib")
def send_sc153_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC153", system="IIB")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"])
    return api_client.send_get_request(endpoint, headers=payload["header"], raise_on_error=False)


@when("I send SC153 request to Azure endpoint", target_fixture="response_azure")
def send_sc153_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC153", system="AZURE")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"])
    return api_client.send_get_request(endpoint, headers=payload["header"], raise_on_error=False)

# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC153")
def compare_sc153_responses(api_client, response_iib, response_azure):
    iib_body, iib_status = response_iib
    azure_body, azure_status = response_azure

    if 401 in (iib_status, azure_status):
        assert iib_status == azure_status, f"SC153 status mismatch: IIB={iib_status}, Azure={azure_status}"
        assert iib_body.strip() == azure_body.strip(), "SC153 unauthorized response body mismatch"
        return

    api_client.compare_json_responses(response_iib, response_azure, "SC153")
