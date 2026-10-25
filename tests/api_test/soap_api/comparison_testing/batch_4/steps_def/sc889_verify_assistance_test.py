import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc889_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC889 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4315", "User Story")
@scenario("Compare SC889 successful responses between IIB and Azure")
def test_compare_sc889_successful_responses():
    """Compare SC889 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC889 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4315", "User Story")
@scenario("Compare SC889 assistance verification failures between IIB and Azure")
def test_compare_sc889_assistance_verification_failures():
    """Compare SC889 assistance verification failures between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC889 api payload for {condition}"), target_fixture="payload")
def create_sc889_payload(condition):
    return sc889_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC889 request to IIB endpoint", target_fixture="response_iib")
def send_sc889_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC889", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC889 request to Azure endpoint", target_fixture="response_azure")
def send_sc889_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC889", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC889")
def compare_sc889_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(
        response_iib, response_azure, "SC889", ignore_element_order=True, trim_message_whitespace=True
    )
