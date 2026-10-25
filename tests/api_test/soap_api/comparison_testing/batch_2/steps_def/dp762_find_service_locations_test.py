from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp762_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP762 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3960", "User Story")
@scenario("Compare DP762 successful response")
def test_compare_dp762_successful_response():
    """Compare DP762 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP762 responses for client with no id verification
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3960", "User Story")
@scenario("Compare DP762 responses for no service locations found")
def test_compare_dp762_response_for_no_service_locations_found():
    """Compare DP762 responses for no service locations found"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    headers, params = dp762_payload_setup(conditions=conditions)
    payloads = {"headers": headers, "params": params}
    return payloads


@given("I send the request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP762", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(
        endpoint, headers=payload["headers"], params=payload["params"], raise_on_error=False
    )


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP762", system="AZURE")
    return api_client.send_get_request(
        endpoint, headers=payload["headers"], params=payload["params"], raise_on_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(
        response_iib[0], response_azure[0], "DP762", exclude_fields=["requestDateTime", "notes", "streetDirections"]
    )
