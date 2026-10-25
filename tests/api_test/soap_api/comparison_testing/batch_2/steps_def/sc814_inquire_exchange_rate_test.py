import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc814_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3972", "User Story")
@scenario("Compare SC814 successful responses between IIB and Azure")
def test_compare_sc814_successful_responses():
    """Compare SC814 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Invalid request
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3972", "API-3972")
@scenario("Compare SC814 invalid request response between IIB and Azure")
def test_compare_sc814_invalid_request_response():
    """Compare SC814 invalid request response between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Invalid country code
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3972", "API-3972")
@scenario("Compare SC814 response for an invalid country code between IIB and Azure")
def test_compare_sc814_invalid_country_code_response():
    """Compare SC814 response for an invalid country code between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC814 api payload for {condition}"), target_fixture="payload")
def create_sc814_payload(condition):
    return sc814_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC814 request to IIB endpoint", target_fixture="response_iib")
def send_sc814_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC814", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC814 request to Azure endpoint", target_fixture="response_azure")
def send_sc814_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC814", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC814")
def compare_sc814_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC814", ignore_element_order=True)
