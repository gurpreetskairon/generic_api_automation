import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc823_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC823 transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3515", "User Story")
@scenario("Compare SC823 transaction responses between IIB and Azure")
def test_compare_sc823_transaction_responses():
    """Compare successful and unsuccessful SC823 transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC823 unrecognised-user response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3515", "User Story")
@scenario("Compare SC823 response for an unrecognised user")
def test_compare_sc823_unrecognised_user_response():
    """Compare the SC823 unrecognised-user response from IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC823 client-validation responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3515", "User Story")
@scenario("Compare SC823 client validation responses between IIB and Azure")
def test_compare_sc823_client_validation_responses():
    """Compare SC823 client-validation responses from IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC823 invalid-request responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3515", "User Story")
@scenario("Compare SC823 invalid request responses between IIB and Azure")
def test_compare_sc823_invalid_request_responses():
    """Compare SC823 invalid-request responses from IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC823 api payload for {condition}"), target_fixture="payload")
def create_sc823_payload_for_condition(condition):
    return sc823_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC823 request to IIB endpoint", target_fixture="response_iib")
def send_sc823_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC823", system="IIB")

    return api_client.send_post_request(
        endpoint,
        payload=payload["request_body"],
        headers=payload["header"],
        raise_error=payload.get("raise_error", True)
    )


@when("I send SC823 request to Azure endpoint", target_fixture="response_azure")
def send_sc823_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC823", system="AZURE")

    return api_client.send_post_request(
        endpoint,
        payload=payload["request_body"],
        headers=payload["header"],
        raise_error=payload.get("raise_error", True)
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC823")
def compare_sc823_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(
        response_iib, response_azure, "SC823", ignore_element_order=True, ignore_tags=["id"]
    )
