import logging
from json import JSONDecodeError

import allure
from pytest_bdd import given, parsers, then, when

from apps.services.integration_soap.payload_data.sc834 import remove_used_notification_ids
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp834_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC702 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4137", "User Story")
@scenario("Compare DP834 successful responses between IIB and Azure")
def test_compare_dp834_successful_responses():
    """Compare DP834 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC702 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4137", "User Story")
@scenario("Compare DP834 negative response between IIB and Azure")
def test_compare_dp834_negative_response():
    """Compare DP834 negative response between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP834 api payload for {condition}"), target_fixture="payload")
def create_dp834_payload(condition):
    iib_payload = dp834_payload_setup(condition=condition)
    azure_payload = dp834_payload_setup(condition=condition, current_notification_id=iib_payload[2])
    return iib_payload, azure_payload


@when("I send DP834 request to IIB endpoint", target_fixture="response_iib")
def send_dp834_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP834", system="IIB", sub_system="MYMSD")
    return api_client.send_post_request(
        endpoint, payload=payload[0][1], headers=payload[0][0], params=payload[0][2]
    ), payload[0][3]


@when("I send DP834 request to Azure endpoint", target_fixture="response_azure")
def send_dp834_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP834", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload[1][1], headers=payload[1][0], params=payload[1][2]
    ), payload[1][3]


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP834")
def compare_dp834_responses(api_client, response_iib, response_azure):
    try:
        remove_used_notification_ids(response_iib[0][0], response_iib[1])
        remove_used_notification_ids(response_azure[0][0], response_azure[1])
    except Exception as e:
        logging.info(f"failed to remove used notifications with error: {e}")

    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP834")
