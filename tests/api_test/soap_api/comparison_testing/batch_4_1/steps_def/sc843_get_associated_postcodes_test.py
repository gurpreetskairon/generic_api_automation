
import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc843_payload_setup
from utils.bdd_utils.scenario import scenario


# ============================================================================
# Scenario 1 - Compare SC843 successful transaction response
# ============================================================================
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4910",
    "API-4910",
)
@scenario("Compare SC843 successful transaction response")
def test_compare_sc843_successful_transaction_response():
    """Compare SC843 successful and no matching record responses."""


# ============================================================================
# Scenario 2 - Compare SC843 invalid search criteria response
# ============================================================================
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4910",
    "API-4910",
)
@scenario("Compare SC843 invalid search criteria response")
def test_compare_sc843_invalid_search_criteria_response():
    """Compare SC843 invalid search criteria response."""


# ============================================================================
# Given steps
# ============================================================================
@given(
    parsers.parse("I create the SC843 api payload for {condition}"),
    target_fixture="payload",
)
def create_payload(condition):
    return sc843_payload_setup(condition=condition)


# ============================================================================
# When steps
# ============================================================================
@when("I send SC843 request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC843", system="IIB")

    return api_client.send_post_request(
        endpoint,
        headers=payload["header"],
        payload=payload["request_body"],
        raise_error=False,
    )


@when("I send SC843 request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC843", system="AZURE")

    return api_client.send_post_request(
        endpoint,
        headers=payload["header"],
        payload=payload["request_body"],
        raise_error=False,
    )


# ============================================================================
# Then steps
# ============================================================================
@then("I can see all the responses are identical for SC843")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(
        response_iib,
        response_azure,
        "SC843",
    )
