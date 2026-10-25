import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp886_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP886 successful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4262", "User Story")
@scenario("Compare DP886 successful responses between DataPower and Azure")
def test_compare_dp886_successful_responses():
    """Compare DP886 successful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP886 unsuccessful responses between DataPower and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4262", "User Story")
@scenario("Compare DP886 unsuccessful responses between DataPower and Azure")
def test_compare_dp886_unsuccessful_responses():
    """Compare DP886 unsuccessful responses between DataPower and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP886 api request for {condition}"), target_fixture="payload")
def create_dp886_payload(condition):
    return dp886_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP886 request to DataPower endpoint", target_fixture="response_iib")
def send_dp886_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP886", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


@when("I send DP886 request to Azure endpoint", target_fixture="response_azure")
def send_dp886_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP886", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP886")
def validate_dp886_response(api_client, response_iib, response_azure):
    # requestDateTime is excluded from strict comparison after the 15-second tolerance check,
    # so larger differences will still fail.
    api_client.compare_json_datetime_tolerance(
        response_iib, response_azure, "dp886", "header.requestDateTime", tolerance_seconds=15
    )
    api_client.compare_json_responses(
        response_iib, response_azure, "dp886", ignore_array_order=True, exclude_fields=["requestDateTime"]
    )
