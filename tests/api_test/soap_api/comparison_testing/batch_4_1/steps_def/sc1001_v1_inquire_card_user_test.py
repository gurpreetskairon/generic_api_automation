import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc1001_v1_payload_setup
from utils.bdd_utils.scenario import scenario


@pytest.mark.skip("The release date for this service has been delayed")
# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC1001 V1 successful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3618", "API-3618")
@scenario("Compare SC1001 V1 successful transaction responses")
def test_compare_sc1001_v1_successful_transaction_responses():
    """Compare SC1001 V1 successful transaction responses."""


@pytest.mark.skip("The release date for this service has been delayed")
# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC1001 V1 invalid request responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3618", "API-3618")
@scenario("Compare SC1001 V1 invalid request responses")
def test_compare_sc1001_v1_invalid_request_responses():
    """Compare SC1001 V1 invalid request responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse("I create the correct SC1001 V1 api payload with different {conditions}"), target_fixture="payload"
)
def create_sc1001_v1_payload_with_condition(conditions):
    return sc1001_v1_payload_setup(conditions)


@given("I send the SC1001 V1 request to IIB endpoint", target_fixture="response_iib")
def send_sc1001_v1_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC1001", system="IIB")

    return api_client.send_post_request(
        url=endpoint, payload=payload["request_body"], headers=payload["header"], json_payload=True
    )


@given("I send the SC1001 V1 request to Azure endpoint", target_fixture="response_azure")
def send_sc1001_v1_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC1001", system="AZURE")

    return api_client.send_post_request(
        url=endpoint, payload=payload["request_body"], headers=payload["header"], json_payload=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC1001 V1")
def compare_all_sc1001_v1_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "SC1001V1", ignore_array_order=True)
