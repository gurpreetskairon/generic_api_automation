import allure
from pytest_bdd import given, parsers, then, when

from apps.services.integration_soap.payload_data.sc595 import sc595_update_endpoint
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc595_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC595 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3936", "User Story")
@scenario("Compare SC595 successful responses between IIB and Azure")
def test_compare_sc595_successful_responses():
    """Compare SC595 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC595 api payload for {condition}"), target_fixture="payload")
def create_sc595_payload(condition):
    return sc595_payload_setup(), condition


# ══════════════════════════════════════════════════════════════════════════════════════
# When Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC595 request to IIB endpoint", target_fixture="response_iib")
def send_sc595_request_to_iib(api_client, payload):
    base_endpoint = build_api_endpoint("SC595", system="IIB")
    endpoint = sc595_update_endpoint(base_endpoint, payload[1])
    return api_client.send_get_request(endpoint, headers=payload[0])


@when("I send the SC595 request to Azure endpoint", target_fixture="response_azure")
def send_sc595_request_to_azure(api_client, payload):
    base_endpoint = build_api_endpoint("SC595", system="AZURE")
    endpoint = sc595_update_endpoint(base_endpoint, payload[1])
    return api_client.send_get_request(endpoint, headers=payload[0], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC595")
def compare_sc595_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(
        response_iib, response_azure, "SC595", ignore_array_order=True, exclude_fields="requestDateTime"
    )
