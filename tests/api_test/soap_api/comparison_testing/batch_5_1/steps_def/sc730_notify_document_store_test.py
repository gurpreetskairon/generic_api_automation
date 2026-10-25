import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc730_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC730 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4310", "User Story")
@scenario("Compare SC730 successful responses between IIB and Azure")
def test_compare_sc730_successful_responses():
    """Compare SC730 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC730 document validation responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4310", "User Story")
@scenario("Compare SC730 document validation responses between IIB and Azure")
def test_compare_sc730_document_validation_responses():
    """Compare SC730 document validation responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC730 request validation responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4310", "User Story")
@scenario("Compare SC730 request validation responses between IIB and Azure")
def test_compare_sc730_request_validation_responses():
    """Compare SC730 request validation responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC730 user validation responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4310", "User Story")
@scenario("Compare SC730 user validation responses between IIB and Azure")
def test_compare_sc730_user_validation_responses():
    """Compare SC730 user validation responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC730 api payload for {condition}"), target_fixture="payload")
def create_sc730_payload(condition):
    return sc730_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC730 request to IIB endpoint", target_fixture="response_iib")
def send_sc730_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC730", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body_iib"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC730 request to Azure endpoint", target_fixture="response_azure")
def send_sc730_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC730", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body_azure"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC730")
def compare_sc730_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC730", ignore_element_order=True)
