import allure
from pytest_bdd import given, parsers, then, when

from apps.services.integration_soap.payload_data.sc831.sc831 import upload_notification_id_to_sc834_db
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc831_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC831 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4159", "User Story")
@scenario("Compare SC831 successful responses between IIB and Azure")
def test_compare_sc831_successful_responses():
    """Compare SC831 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC831 negative responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4159", "User Story")
@scenario("Compare SC831 negative responses between IIB and Azure")
def test_compare_sc831_negative_responses():
    """Compare SC831 negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC831 api {payload} payload for {condition}"), target_fixture="payload")
def create_sc831_payload(condition, payload):
    return sc831_payload_setup(condition=condition, payload_type=payload)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC831 request to IIB endpoint", target_fixture="response_iib")
def send_sc831_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC831", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0]), payload[2]


@when("I send SC831 request to Azure endpoint", target_fixture="response_azure")
def send_sc831_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC831", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0]), payload[2]


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I can see all the responses are identical for SC831 {condition}"))
def compare_sc831_responses(api_client, response_iib, response_azure, condition):
    if condition == "transaction_successful":
        upload_notification_id_to_sc834_db(response_iib[0][0], response_iib[1])
        upload_notification_id_to_sc834_db(response_azure[0][0], response_azure[1])
    api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC831", ignore_element_order=True, ignore_tags=["value"])
