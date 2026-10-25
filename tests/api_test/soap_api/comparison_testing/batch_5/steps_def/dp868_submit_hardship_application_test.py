import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp868_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP868 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4264", "API-4264")
@scenario("Compare DP868 successful transaction response")
def test_compare_dp868_successful_transaction_response():
    """Compare DP868 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct DP868 api payload with different {conditions}"), target_fixture="payload")
def create_dp868_payload_with_condition(conditions):
    return dp868_payload_setup(conditions)


@given("I send the DP868 request to IIB endpoint", target_fixture="response_iib")
def send_dp868_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP868", system="IIB", sub_system="MYMSD")

    return api_client.send_post_request(
        endpoint,
        payload=payload["request_body"],
        headers=payload["header"],
        params=payload["params"],
        json_payload=True
    )


@given("I send the DP868 request to Azure endpoint", target_fixture="response_azure")
def send_dp868_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("DP868", system="AZURE")

    return api_client.send_post_request(
        endpoint,
        payload=payload["request_body"],
        headers=payload["header"],
        params=payload["params"],
        json_payload=True,
        raise_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP868")
def compare_all_dp868_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP868", exclude_fields=["objectRefs"])
