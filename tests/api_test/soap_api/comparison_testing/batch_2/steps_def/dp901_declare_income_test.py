import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp901_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP901 successful income declaration responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3957", "User Story")
@scenario("Compare DP901 successful response for income declaration")
def test_compare_dp901_successful_income_declaration():
    """Compare DP901 successful income declaration responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP901 unrecognised income type response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3957", "User Story")
@scenario("Compare DP901 response for unrecognised income type code")
def test_compare_dp901_unrecognised_income_type_code():
    """Compare DP901 unrecognised income type response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the api payload for {condition}"), target_fixture="payload")
def create_payload(condition):
    return dp901_payload_setup(condition=condition)


@given("I send manage income request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP901", system="IIB", sub_system="MYMSD")
    return api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True
    )


@given("I send manage income request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP901", system="AZURE")
    return api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the DP901 responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "dp901")
