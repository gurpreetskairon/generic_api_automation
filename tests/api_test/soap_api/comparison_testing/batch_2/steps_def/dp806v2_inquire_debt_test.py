import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp806_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP806V2 successful response for debt details
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3956/", "User Story")
@scenario("Compare DP806V2 successful response for debt details")
def test_compare_dp806v2_successful_response_for_debt_details():
    """Compare DP806V2 successful response for debt details"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP806V2 no matching record response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3956", "User Story")
@scenario("Compare DP806V2 response when no matching debt record exists")
def test_compare_dp806v2_no_matching_record_response():
    """Compare DP806V2 response when no matching debt record exists"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the api payload for {condition}"), target_fixture="payload")
def create_payload(condition):
    return dp806_payload_setup(condition=condition)


@given("I send inquire debt request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP806", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


@given("I send inquire debt request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP806", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(
        response_iib, response_azure, "dp806", exclude_fields=["incurredFrom"], ignore_array_order=True
    )
