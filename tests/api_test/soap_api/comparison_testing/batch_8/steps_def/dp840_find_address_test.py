import allure
from pytest_bdd import given, parsers, then, when
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp840_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP840 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════

@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4527", "User Story")
@scenario("Compare DP840 successful responses between IIB and Azure")
def test_compare_dp840_successful_responses():
    """Compare DP840 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP840 invalid search responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════

# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4527", "User Story")
# @scenario("Compare DP840 invalid search responses between IIB and Azure")
# def test_compare_dp840_invalid_data_responses():
#     """Compare DP840 invalid search responses between IIB and Azure"""

# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════

@given(parsers.parse("I create the DP840 api payload for {condition}"), target_fixture="payload")
def create_dp840_payload(condition):
    return dp840_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════

@when("I send DP840 request to IIB endpoint", target_fixture="response_iib")
def send_dp840_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP840", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


@when("I send DP840 request to Azure endpoint", target_fixture="response_azure")
def send_dp840_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP840", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════

@then("I can see all the responses are identical for DP840")
def compare_dp840_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP840", exclude_fields=["requestDateTime"])
