import allure
from pytest_bdd import given, parsers, then, when

from apps.services.integration_soap.payload_data.dp595 import dp595_update_endpoint
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp595_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP595 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3936", "User Story")
@scenario("Compare DP595 successful responses between IIB and Azure")
def test_compare_dp595_successful_responses():
    """Compare DP595 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP595 api payload for {condition}"), target_fixture="payload")
def create_dp595_payload(condition):
    return dp595_payload_setup()


@when("I send the DP595 request to IIB endpoint", target_fixture="response_iib")
def send_dp595_request_to_iib(api_client, payload):
    base_endpoint = build_api_endpoint("DP595", system="IIB", sub_system="MYMSD")
    endpoint = dp595_update_endpoint(base_endpoint)
    return api_client.send_get_request(endpoint, headers=payload)


@when("I send the DP595 request to Azure endpoint", target_fixture="response_azure")
def send_dp595_request_to_azure(api_client, payload):
    base_endpoint = build_api_endpoint("DP595", system="AZURE")
    endpoint = dp595_update_endpoint(base_endpoint)
    return api_client.send_get_request(endpoint, headers=payload, raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP595")
def compare_dp595_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(
        response_iib, response_azure, "DP595", ignore_array_order=True, exclude_fields="requestDateTime"
    )
