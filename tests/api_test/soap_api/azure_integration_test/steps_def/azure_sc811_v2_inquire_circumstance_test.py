from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc811_v2_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check SC811 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-XXXX", "API-XXXX")
@scenario("Check SC811 successful transaction response")
def test_sc811_successful_transaction_response():
    """Check SC811 successful transaction response"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check SC811 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-XXXX", "API-XXXX")
@scenario("Check SC811 unsuccessful transaction response")
def test_sc811_unsuccessful_transaction_response():
    """Check SC811 unsuccessful transaction response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the correct payload for SC811 with "{condition}"'), target_fixture="payload")
def create_correct_payload(condition):
    return sc811_v2_payload_setup(condition)


@given(parsers.parse('I create the payload for SC811 with "{condition}"'), target_fixture="payload")
def create_payload(condition):
    return sc811_v2_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC811 request to the Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC811V2", system="AZURE")

    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse('I can see the SC811 result code as "{result_code}"'))
def validate_result_code(api_client, response_azure, result_code):
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see the SC811 result message as "{result_message}"'))
def validate_result_message(api_client, response_azure, payload, result_message):
    if "<user code>" in result_message:
        user_id = payload["scenario_data"]["user_id"]
        result_message = result_message.replace("<user code>", user_id)

        if not result_message.endswith("."):
            result_message = result_message + "."

    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.result_message, result_message)
