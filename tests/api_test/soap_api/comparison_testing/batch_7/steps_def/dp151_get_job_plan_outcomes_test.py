import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp151_payload_setup
from utils.bdd_utils.scenario import scenario

# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC151 successful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4626", "User Story")
@scenario("Compare DP151 successful responses between DataPower and Azure")
def test_compare_dp151_successful_responses():
    """Compare DP151 successful responses between DataPower and Azure"""

# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC151 unsuccessful responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4626", "User Story")
@scenario("Compare DP151 bad request responses between DataPower and Azure")
def test_compare_dp151_bad_request_responses():
    """Compare DP151 bad request responses between DataPower and Azure"""

# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP151 api payload for {condition}"), target_fixture="payload")
def create_dp151_payload(condition):
    return dp151_payload_setup(condition=condition)

# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send DP151 request to DataPower endpoint", target_fixture="response_iib")
def send_dp151_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP151", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload["header"], params=payload["params"], raise_on_error=False)


@when("I send DP151 request to Azure endpoint", target_fixture="response_azure")
def send_dp151_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP151", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload["header"], params=payload["params"], raise_on_error=False)

# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP151")
def compare_dp151_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP151", ignore_array_order=True)
