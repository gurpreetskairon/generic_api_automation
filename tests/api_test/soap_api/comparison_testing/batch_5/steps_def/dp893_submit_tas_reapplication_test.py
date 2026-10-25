import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp893_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP893 successful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4265", "User Story")
@scenario("Compare DP893 successful responses between DataPower and Azure")
def test_compare_dp893_successful_responses():
    """Compare DP893 successful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP893 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4265", "User Story")
@scenario("Compare DP893 unsuccessful responses between DataPower and Azure")
def test_compare_dp893_unsuccessful_responses():
    """Compare DP893 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP893 api request for {condition}"), target_fixture="payload")
def create_dp893_payload(condition):
    return dp893_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP893 request to DataPower endpoint", target_fixture="response_iib")
def send_dp893_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP893", system="IIB", sub_system="MYMSD")
    return api_client.send_post_request(
        endpoint, payload=payload[2], headers=payload[0], params=payload[1], json_payload=True, raise_error=payload[4]
    )


@when("I send DP893 request to Azure endpoint", target_fixture="response_azure")
def send_dp893_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP893", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload[3], headers=payload[0], params=payload[1], json_payload=True, raise_error=payload[4]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP893")
def validate_dp893_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "dp893", ignore_array_order=True)
