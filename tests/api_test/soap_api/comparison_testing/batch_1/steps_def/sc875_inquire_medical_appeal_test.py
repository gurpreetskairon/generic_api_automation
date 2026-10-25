from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc875_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC875 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3173", "API-3173")
@scenario("Compare SC875 successful transaction response")
def test_compare_sc875_successful_transaction_response():
    """Compare SC875 successful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC875 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3173", "API-3173")
@pytest.mark.skip(reason="SC875 87501 cannot currently be reproduced. Tracked under Test Automation Risk Management.")
@scenario("Compare SC875 unsuccessful transaction response")
def test_compare_sc875_unsuccessful_transaction_response():
    """Compare SC875 unsuccessful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_sc875_payload_with_condition(conditions):
    return sc875_payload_setup(conditions)


@given("I send the SC875 request to IIB endpoint", target_fixture="response_iib")
def send_sc875_request_to_iib_endpoint(api_client, payload):
    iib_endpoint = build_api_endpoint("SC875", system="IIB")

    return api_client.send_post_request(iib_endpoint, payload=payload["request_body"], headers=payload["header"])


@given("I send the SC875 request to Azure endpoint", target_fixture="response_azure")
def send_sc875_request_to_azure_endpoint(api_client, payload):
    azure_endpoint = build_api_endpoint("SC875", system="AZURE")
    payload["header"] = {"Content-Type": "application/xml"}

    return api_client.send_post_request(azure_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC875")
def compare_all_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC875")
