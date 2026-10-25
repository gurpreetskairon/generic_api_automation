import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc161_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC161 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4615", "User Story")
@scenario("Compare SC161 successful responses between IIB and Azure")
def test_compare_sc161_successful_responses():
    """Compare SC161 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC161 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4615", "User Story")
@scenario("Compare SC161 unsuccessful responses between IIB and Azure")
def test_compare_sc161_unsuccessful_responses():
    """Compare SC161 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC161 api payload for {condition}"), target_fixture="payload")
def create_sc161_payload(condition):
    return sc161_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC161 request to IIB endpoint", target_fixture="response_iib")
def send_sc161_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC161", system="IIB")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"])

    return api_client.send_get_request(
        endpoint,
        headers=payload["header"],
        raise_on_error=payload["raise_on_error"],
    )


@when("I send SC161 request to Azure endpoint", target_fixture="response_azure")
def send_sc161_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC161", system="AZURE")
    endpoint = endpoint.replace("{participantId}", payload["participant_id"])

    return api_client.send_get_request(
        endpoint,
        headers=payload["header"],
        raise_on_error=payload["raise_on_error"],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC161")
def compare_sc161_responses(api_client, response_iib, response_azure):
    iib_body, iib_status = response_iib
    azure_body, azure_status = response_azure

    if 401 in (iib_status, azure_status):
        assert iib_status == azure_status, f"SC161 status mismatch: IIB={iib_status}, Azure={azure_status}"
        assert iib_body.strip() == azure_body.strip(), "SC161 unauthorized response body mismatch"
        return

    api_client.compare_json_responses(response_iib, response_azure, "SC161")
