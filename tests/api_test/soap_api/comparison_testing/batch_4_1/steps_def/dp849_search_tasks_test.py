from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp849_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare dp849 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Compare dp849 successful response")
def test_compare_dp849_successful_response():
    """Compare dp849 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare dp849 client not recognised response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3311", "API-3311")
@scenario("Compare dp849 client not recognised response")
def test_compare_dp849_client_not_recognised_response():
    """Compare dp849 client not recognised response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_payload(conditions):
    return dp849_payload_setup(condition=conditions)


@given("I send the inquire provider request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP849", system="IIB", sub_system="MYMSD")
    response = api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True
    )
    return response


@given("I send the inquire provider request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP849", system="AZURE")
    response = api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True
    )
    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "dp849", exclude_fields="requestDateTime")
