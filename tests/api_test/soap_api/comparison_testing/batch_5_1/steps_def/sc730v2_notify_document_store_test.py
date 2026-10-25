import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc730v2_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC730 V2 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4309", "User Story")
@scenario("Compare SC730V2 successful responses between IIB and Azure")
def test_compare_sc730v2_successful_responses():
    """Compare SC730V2 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC730 V2 document validation responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4309", "User Story")
@scenario("Compare SC730V2 document validation responses between IIB and Azure")
def test_compare_sc730v2_document_validation_responses():
    """Compare SC730V2 document validation responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC730 V2 request validation responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4309", "User Story")
@scenario("Compare SC730V2 request validation responses between IIB and Azure")
def test_compare_sc730v2_request_validation_responses():
    """Compare SC730V2 request validation responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC730V2 user validation responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4309", "User Story")
@scenario("Compare SC730V2 security validation responses between IIB and Azure")
def test_compare_sc730v2_security_validation_responses():
    """Compare SC730V2 security validation responses between IIB and Azure"""

# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC730V2 api payload for {condition}"), target_fixture="payload")
def create_sc730v2_payload(condition):
    return sc730v2_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC730V2 request to IIB endpoint", target_fixture="response_iib")
def send_sc730v2_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC730V2", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body_iib"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC730V2 request to Azure endpoint", target_fixture="response_azure")
def send_sc730_v2_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC730V2", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body_azure"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC730V2")
def compare_sc730v2_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC730V2", ignore_element_order=True)
