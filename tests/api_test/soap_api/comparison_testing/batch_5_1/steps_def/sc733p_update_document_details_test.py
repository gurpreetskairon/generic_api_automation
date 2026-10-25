import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc733p_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC733P successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4313", "User Story")
@scenario("Compare SC733P successful responses between IIB and Azure")
def test_compare_sc733p_successful_responses():
    """Compare SC733P successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC733P unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4313", "User Story")
@scenario("Compare SC733P unsuccessful responses between IIB and Azure")
def test_compare_sc733p_unsuccessful_responses():
    """Compare SC733P unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC733P api payload for {condition}"), target_fixture="payload")
def create_sc733p_payload(condition):
    return sc733p_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC733P request to IIB endpoint", target_fixture="response_iib")
def send_sc733p_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC733P", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@when("I send SC733P request to Azure endpoint", target_fixture="response_azure")
def send_sc733p_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC733P", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC733P")
def compare_sc733p_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC733P", ignore_element_order=True,
                                      ignore_tags=["faultcode", "errorCode"], ignore_schema_parser_location=True)
