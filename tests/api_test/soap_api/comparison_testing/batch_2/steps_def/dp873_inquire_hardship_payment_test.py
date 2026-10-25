import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp873_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Supported client types with hardship payment records
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 successful response for supported client types")
def test_compare_dp873_successful_response_for_supported_client_types():
    """Compare dp873 responses for supported client types."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - No hardship payment recorded
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response when no hardship payment is recorded")
def test_compare_dp873_response_when_no_hardship_payment_is_recorded():
    """Compare dp873 responses when no hardship payment is recorded."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Secured client
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response for a secured client")
def test_compare_dp873_response_for_secured_client():
    """Compare dp873 responses for a secured client."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Client without partner
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response when the client does not have a partner")
def test_compare_dp873_response_when_client_does_not_have_partner():
    """Compare dp873 responses when partner inclusion is requested but no partner exists."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Partner without hardship payment
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response when the partner has no hardship payment")
def test_compare_dp873_response_when_partner_has_no_hardship_payment():
    """Compare dp873 responses when the partner has no hardship payment."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 6 - Unrecognised user or source system
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response for an unrecognised user or source system")
def test_compare_dp873_response_for_unrecognised_user_or_source_system():
    """Compare dp873 responses for an unrecognised user or source system."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 7 - Unrecognised client
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response for an unrecognised client")
def test_compare_dp873_response_for_unrecognised_client():
    """Compare dp873 responses for an unrecognised client."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 8 - Schema-validation conditions
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 schema-validation responses")
def test_compare_dp873_schema_validation_responses():
    """Compare dp873 responses for invalid client-number and date formats."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 9 - Missing minimum request data
# ══════════════════════════════════════════════════════════════════════════════
@pytest.mark.skip("unable to figure out correct payload for this scenario")
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response when minimum request data is missing")
def test_compare_dp873_response_when_minimum_request_data_is_missing():
    """Compare dp873 responses when mandatory request data is missing."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 10 - Partner inclusion set to false
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare DP873 response when partner hardship payment is not requested")
def test_compare_dp873_response_when_partner_hardship_payment_is_not_requested():
    """Compare dp873 responses when partner inclusion is false."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct dp873 api payload for {client_type}"), target_fixture="payload")
def create_correct_dp873_payload_for_client_type(client_type):
    return dp873_payload_setup(client_type)


@given(parsers.parse("I create the dp873 api payload for {condition}"), target_fixture="payload")
def create_dp873_payload_for_condition(condition):
    return dp873_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send dp873 inquire hardship payment request to IIB endpoint", target_fixture="response_iib")
def send_dp873_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP873", system="IIB", sub_system="MYMSD")
    response = api_client.send_get_request(endpoint, headers=payload[0], params=payload[1], raise_on_error=False)
    return response


@when("I send dp873 inquire hardship payment request to Azure endpoint", target_fixture="response_azure")
def send_dp873_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP873", system="AZURE")
    response = api_client.send_get_request(endpoint, headers=payload[0], params=payload[1], raise_on_error=False)
    return response


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for dp873")
def compare_dp873_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP873", exclude_fields="subResults")
