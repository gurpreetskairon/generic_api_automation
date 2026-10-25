import allure
from pytest_bdd import given, parsers, then, when
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp896_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP896 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4145", "User Story")
@scenario("Compare DP896 successful responses between IIB and Azure")
def test_compare_dp896_successful_responses():
    """Compare DP896 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC852 invalid responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4145", "User Story")
@scenario("Compare DP896 invalid responses between IIB and Azure")
def test_compare_dp896_invalid_responses():
    """Compare DP896 invalid responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP896 api payload for {condition}"), target_fixture="payload")
def create_dp896_payload(condition):
    return dp896_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send DP896 request to IIB endpoint", target_fixture="response_iib")
def send_dp896_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP896", system="IIB", sub_system="MYMSD")
    return api_client.send_post_request(
        endpoint, payload=payload[2], headers=payload[0], params=payload[1], raise_error=False
    )


@when("I send DP896 request to Azure endpoint", target_fixture="response_azure")
def send_dp896_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP896", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload[2], headers=payload[0], params=payload[1], raise_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP896")
def compare_dp896_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP896", ignore_array_order=True)
