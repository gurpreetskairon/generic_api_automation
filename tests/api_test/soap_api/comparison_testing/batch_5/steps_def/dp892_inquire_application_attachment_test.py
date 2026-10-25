import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp892_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP892 successful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4258", "User Story")
@scenario("Compare DP892 successful responses between DataPower and Azure")
def test_compare_dp892_successful_responses():
    """Compare DP892 successful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP892 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4258", "User Story")
@scenario("Compare DP892 unsuccessful responses between DataPower and Azure")
def test_compare_dp892_unsuccessful_responses():
    """Compare DP892 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP892 api request for {condition}"), target_fixture="payload")
def create_dp892_payload(condition):
    return dp892_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP892 request to DataPower endpoint", target_fixture="response_iib")
def send_dp892_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP892", system="IIB", sub_system="MYMSD")
    response = api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])

    allure.attach(response[0], name="DataPower Response", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(response[1]), name="DataPower Status Code", attachment_type=allure.attachment_type.TEXT)

    return response


# TODO: Temporary DataPower-only validation until DP892 Azure development is complete.
# Restore the Azure request step and normal comparison once the Azure endpoint is available.

# @when("I send DP892 request to Azure endpoint", target_fixture="response_azure")
# def send_dp892_request_to_azure():
#     pytest.skip("DP892 Azure development is not yet available")


@when("I send DP892 request to Azure endpoint", target_fixture="response_azure")
def send_dp892_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP892", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP892")
def validate_dp892_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "dp892", ignore_array_order=True)
