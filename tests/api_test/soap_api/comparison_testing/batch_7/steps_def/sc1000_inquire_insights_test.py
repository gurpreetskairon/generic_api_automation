import allure
from pytest_bdd import given, parsers, then
from apps.services.integration_soap.payload_data.sc1000 import update_endpoint_client
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc1000_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC1000 successful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3618", "API-3618")
@scenario("Compare SC1000 successful transaction responses")
def test_compare_sc1000_successful_transaction_responses():
    """Compare SC1000 successful transaction responses."""



# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC1000 api payload with different {conditions}"), target_fixture="payload")
def create_sc1000_payload_with_condition(conditions):
    return sc1000_payload_setup(conditions)


@given("I send the SC1000 request to IIB endpoint", target_fixture="response_iib")
def send_sc1000_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC1000", system="IIB")
    endpoint = update_endpoint_client(endpoint, payload[2][1])
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1], raise_on_error=False)


@given("I send the SC1000 request to Azure endpoint", target_fixture="response_azure")
def send_sc1000_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC1000", system="AZURE")
    endpoint = update_endpoint_client(endpoint, payload[2][1])
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC1000")
def compare_all_sc1000_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "SC1000", ignore_array_order=True)
