import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc816_payload_setup
from utils.bdd_utils.scenario import scenario


@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-XXXX", "User Story")
@scenario("Compare SC816 successful responses between IIB and Azure")
def test_compare_sc816_successful_responses():
    """Compare SC816 successful responses between IIB and Azure"""


@given(parsers.parse("I create the SC816 api payload for {condition}"), target_fixture="payload")
def create_sc816_payload(condition):
    return sc816_payload_setup(condition=condition)


@when("I send SC816 request to IIB endpoint", target_fixture="response_iib")
def send_sc816_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC816", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC816 request to Azure endpoint", target_fixture="response_azure")
def send_sc816_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC816", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@then("I can see all the responses are identical for SC816")
def compare_sc816_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC816", ignore_element_order=True)
