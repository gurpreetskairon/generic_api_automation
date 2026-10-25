import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc873_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Supported client types with hardship payment records
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 successful response for supported client types")
def test_compare_sc873_successful_response_for_supported_client_types():
    """Compare SC873 responses for supported client types."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - No hardship payment recorded
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response when no hardship payment is recorded")
def test_compare_sc873_response_when_no_hardship_payment_is_recorded():
    """Compare SC873 responses when no hardship payment is recorded."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Secured client
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response for a secured client")
def test_compare_sc873_response_for_secured_client():
    """Compare SC873 responses for a secured client."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Client without partner
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response when the client does not have a partner")
def test_compare_sc873_response_when_client_does_not_have_partner():
    """Compare SC873 responses when partner inclusion is requested but no partner exists."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Partner without hardship payment
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response when the partner has no hardship payment")
def test_compare_sc873_response_when_partner_has_no_hardship_payment():
    """Compare SC873 responses when the partner has no hardship payment."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 6 - Unrecognised user or source system
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response for an unrecognised user or source system")
def test_compare_sc873_response_for_unrecognised_user_or_source_system():
    """Compare SC873 responses for an unrecognised user or source system."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 7 - Unrecognised client
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response for an unrecognised client")
def test_compare_sc873_response_for_unrecognised_client():
    """Compare SC873 responses for an unrecognised client."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 8 - Schema-validation conditions
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 schema-validation responses")
def test_compare_sc873_schema_validation_responses():
    """Compare SC873 responses for invalid client-number and date formats."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 9 - Missing minimum request data
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response when minimum request data is missing")
def test_compare_sc873_response_when_minimum_request_data_is_missing():
    """Compare SC873 responses when mandatory request data is missing."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 10 - Partner inclusion set to false
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3505", "User Story")
@scenario("Compare SC873 response when partner hardship payment is not requested")
def test_compare_sc873_response_when_partner_hardship_payment_is_not_requested():
    """Compare SC873 responses when partner inclusion is false."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the correct SC873 api payload for {client_type}"), target_fixture="payload")
def create_correct_sc873_payload_for_client_type(client_type):
    return sc873_payload_setup(client_type)


@given(parsers.parse("I create the SC873 api payload for {condition}"), target_fixture="payload")
def create_sc873_payload_for_condition(condition):
    return sc873_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC873 inquire hardship payment request to IIB endpoint", target_fixture="response_iib")
def send_sc873_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC873", system="IIB")
    response_text, status_code = api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
    )
    return response_text


@when("I send SC873 inquire hardship payment request to Azure endpoint", target_fixture="response_azure")
def send_sc873_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC873", system="AZURE")
    response_text, status_code = api_client.send_post_request(
        endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
    )
    return response_text


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC873")
def compare_sc873_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(
        response_iib,
        response_azure,
        "SC873",
        ignore_element_order=True,
        ignore_tags=["faultcode"],
        ignore_schema_parser_location=True
    )
