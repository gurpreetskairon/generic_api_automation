import allure
from pytest_bdd import given, parsers, then, when

from apps.services.integration_soap.payload_data.dp825 import compare_dp825_responses, url_azure, url_iib
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp825_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check whether the DP825 responses are the same across different endpoints
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3626", "User Story")
@scenario("Check whether the DP825 responses are the same across different endpoints")
def test_check_dp825_positive():
    """Check whether the DP825 responses are the same across different endpoints"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check responses across different endpoints with different conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3626", "User Story")
@scenario("Check DP825 responses are the same across different endpoints with different conditions")
def test_check_dp825_different_conditions():
    """Check DP825 responses are the same across different endpoints with different conditions"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the DP825 request for "{condition}"'), target_fixture="payload")
def create_dp825_request(condition, formatted_datetime):
    return dp825_payload_setup(condition=condition, date_time=formatted_datetime)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the DP825 request to the IIB endpoint", target_fixture="response_iib")
def send_dp825_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP825", system="IIB", sub_system="MYMSD")
    request_url = url_iib(endpoint, payload)
    return api_client.send_get_request(request_url, headers=payload["iib_headers"], raise_on_error=False)


@when("I send the same DP825 request to the Azure endpoint", target_fixture="response_azure")
def send_dp825_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP825", system="AZURE", sub_system="NONE")
    request_url = url_azure(endpoint, payload)
    return api_client.send_get_request(request_url, headers=payload["azure_headers"], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the DP825 responses are identical")
def validate_dp825_responses(api_client, response_iib, response_azure):
    compare_dp825_responses(api_client, response_iib, response_azure)
