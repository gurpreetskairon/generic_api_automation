import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc810v2_payload_setup
from utils.bdd_utils.scenario import scenario


@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-XXXX", "User Story")
@scenario("Compare SC810V2 successful responses between IIB and Azure")
def test_compare_sc810v2_successful_responses():
    """Compare SC810V2 successful responses between IIB and Azure"""


@given(parsers.parse("I create the SC810V2 api payload for {condition}"), target_fixture="payload")
def create_sc810v2_payload(condition):
    return sc810v2_payload_setup(condition=condition)


@when("I send SC810V2 request to IIB endpoint", target_fixture="response_iib")
def send_sc810v2_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC810V2", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC810V2 request to Azure endpoint", target_fixture="response_azure")
def send_sc810v2_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC810V2", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@then("I can see all the responses are identical for SC810V2")
def compare_sc810v2_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC810V2", ignore_element_order=True)
