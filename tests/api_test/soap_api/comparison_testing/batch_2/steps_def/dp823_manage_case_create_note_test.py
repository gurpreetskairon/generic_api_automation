import allure
import json
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp823_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP823 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3958", "User Story")
@scenario("Compare DP823 successful transaction response")
def test_compare_dp823_successful_transaction_response():
    """Compare DP823 successful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP823 invalid user credentials response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3958", "User Story")
@scenario("Compare DP823 response for invalid user credentials")
def test_compare_dp823_invalid_user_credentials_response():
    """Compare DP823 invalid user credentials response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare DP823 invalid client number response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3958", "User Story")
@scenario("Compare DP823 response for an invalid client number")
def test_compare_dp823_invalid_client_number_response():
    """Compare DP823 invalid client number response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare DP823 invalid request responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3958", "User Story")
@scenario("Compare DP823 invalid request responses")
def test_compare_dp823_invalid_request_responses():
    """Compare DP823 invalid request responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the api payload for {condition}"), target_fixture="payload")
def create_payload(condition):
    payload = dp823_payload_setup(condition=condition)
    allure.attach(json.dumps(payload[2], ensure_ascii=False, indent=4), name="DP823 Request Payload", attachment_type=allure.attachment_type.JSON)
    return payload


@given("I send create unstructured note request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP823", system="IIB", sub_system="MYMSD")
    return api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True, raise_error=False
    )


@given("I send create unstructured note request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP823", system="AZURE")
    return api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True, raise_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the DP823 responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "dp823")
