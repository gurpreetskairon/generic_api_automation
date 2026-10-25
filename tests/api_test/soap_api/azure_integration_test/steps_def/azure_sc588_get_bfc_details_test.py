import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc588_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify SC588 response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3422", "API-3422")
@scenario("Verify SC588 unauthorized response")
def test_verify_sc588_responses():
    """Verify SC588 unauthorized response."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC588 api payload with different {conditions}"), target_fixture="payload")
def create_sc588_payload_with_condition(conditions):
    return sc588_payload_setup(conditions)



@given("I send the SC588 request to Azure endpoint", target_fixture="response_azure")
def send_sc588_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC588", system="AZURE")

    return api_client.send_get_request(url=endpoint, headers=payload["header"],
                                       params=payload["params"], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC588")
@then("I can see Invalid Credentials displayed in the response")
def compare_all_dp588_responses(api_client, response_azure):
    api_client.compare_status_code("401", str(response_azure[1]))
