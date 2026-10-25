import allure

from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc162_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC162 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4617", "API-4617")
@scenario("Compare SC162 successful transaction response")
def test_compare_sc162_successful_transaction_response():
    """Compare SC162 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC162 report_job_search_not_found
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4617", "API-4617")
@scenario("Compare SC162 invalid request response")
def test_compare_sc162_report_job_search_not_found():
    """Compare SC162 report job search not found."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC162 api request with different {conditions}"), target_fixture="payload")
def create_sc162_request_with_condition(conditions):
    """
    Create the SC162 request payload based on the requested test condition.
    """
    return sc162_payload_setup(conditions)


@given(
    "I send the SC162 request to IIB endpoint",
    target_fixture="response_iib",
)
def send_sc162_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint(
        "SC162",
        system="IIB",
    ).replace(
        "{participantId}",
        payload["participant_id"],
    )

    return api_client.send_rest_put_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
        raise_error=payload["raise_error"],
    )


@given(
    "I send the SC162 request to Azure endpoint",
    target_fixture="response_azure",
)
def send_sc162_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint(
        "SC162",
        system="AZURE",
    ).replace(
        "{participantId}",
        payload["participant_id"],
    )

    return api_client.send_rest_put_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
        raise_error=payload["raise_error"],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC162")
def compare_all_sc162_responses(api_client, response_iib, response_azure):
    """
    Compare the IIB and Azure SC162 responses.
    """
    api_client.compare_json_responses(response_iib, response_azure, "SC162")
