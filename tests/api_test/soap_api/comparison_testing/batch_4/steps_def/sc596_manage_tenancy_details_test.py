import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc596_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC596 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4329", "User Story")
@scenario("Compare SC596 successful responses between IIB and Azure")
def test_compare_sc596_successful_responses():
    """Compare SC596 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC596 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4329", "User Story")
@scenario("Compare SC596 unsuccessful responses between IIB and Azure")
def test_compare_sc596_unsuccessful_responses():
    """Compare SC596 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC596 invalid request parameter responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-XXXX", "User Story")
@scenario("Compare SC596 invalid request parameter responses between IIB and Azure")
def test_compare_sc596_invalid_request_parameter_responses():
    """Compare SC596 invalid request parameter responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC596 api payload for {condition}"), target_fixture="payload")
def create_sc596_payload(condition):
    return sc596_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC596 request to IIB endpoint", target_fixture="response_iib")
def send_sc596_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC596", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["iib_request_body"], headers=payload["header"])


@when("I send SC596 request to Azure endpoint", target_fixture="response_azure")
def send_sc596_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC596", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["azure_request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC596")
def validate_sc596_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(
        response_iib, response_azure, "SC596", exclude_fields=["referenceId"], ignore_array_order=True
    )
