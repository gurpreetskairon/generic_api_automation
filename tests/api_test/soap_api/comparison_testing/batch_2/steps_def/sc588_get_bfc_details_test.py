import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc588_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC588 successful transaction responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3422", "API-3422")
@scenario("Compare SC588 successful transaction responses")
def test_compare_sc588_successful_transaction_responses():
    """Compare SC588 successful transaction responses."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC588 api payload with different {conditions}"), target_fixture="payload")
def create_sc588_payload_with_condition(conditions):
    return sc588_payload_setup(conditions)


@given("I send the SC588 request to IIB endpoint", target_fixture="response_iib")
def send_sc588_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC588", system="IIB")

    return api_client.send_get_request(url=endpoint, headers=payload["header"], params=payload["params"])


@given("I send the SC588 request to Azure endpoint", target_fixture="response_azure")
def send_sc588_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC588", system="AZURE")

    return api_client.send_get_request(url=endpoint, headers=payload["header"], params=payload["params"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC588")
def compare_all_sc588_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(
        response_iib[0], response_azure[0], "SC588", exclude_fields=["message"], ignore_array_order=True
    )
