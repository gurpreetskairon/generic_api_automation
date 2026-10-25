import allure
from pytest_bdd import given, parsers, then, when

from apps.services.integration_soap.payload_data.sc834 import remove_used_notification_ids
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc834_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC834 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4157", "User Story")
@scenario("Compare SC834 successful responses between IIB and Azure")
def test_compare_sc834_successful_responses():
    """Compare SC834 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC834 negative response between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4157", "User Story")
@scenario("Compare SC834 negative response between IIB and Azure")
def test_compare_sc834_negative_response():
    """Compare SC834 negative response between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC834 api payload for {condition}"), target_fixture="payload")
def create_sc834_payload(condition):
    iib_payload = sc834_payload_setup(condition=condition)
    azure_payload = sc834_payload_setup(condition=condition, current_notification_id=iib_payload[2])
    return iib_payload, azure_payload


@when("I send SC834 request to IIB endpoint", target_fixture="response_iib")
def send_sc834_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC834", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[0][1], headers=payload[0][0]), payload[0][2]


@when("I send SC834 request to Azure endpoint", target_fixture="response_azure")
def send_sc834_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC834", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1][1], headers=payload[1][0]), payload[1][2]


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I can see all the responses are identical for SC834 with {condition}"))
def compare_sc834_responses(condition, api_client, response_iib, response_azure):
    if condition != "notification_not_recognised":
        remove_used_notification_ids(response_iib[0][0], response_iib[1])
        remove_used_notification_ids(response_azure[0][0], response_azure[1])


    try:
        api_client.compare_soap_responses(response_iib[0], response_azure[0], "SC834", ignore_element_order=True)
    except Exception as e:
        if condition == "successful_response":
            msg = (f"Test has failed, expected Transaction Successful but got: {e}, "
                   f"data may no longer be valid, run SC831 to create more")
            allure.attach(msg, name="Successful_response Failed", attachment_type=allure.attachment_type.JSON)
            raise Exception(msg)



