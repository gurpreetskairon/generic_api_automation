import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc825_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC825 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2931", "User Story")
@scenario("Compare SC825 successful response")
def test_compare_sc825_successful_response():
    """Compare SC825 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC825 successful result and subresult response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2931", "User Story")
@scenario("Compare SC825 successful result and subresult response")
def test_compare_sc825_successful_result_and_subresult_response():
    """Compare SC825 successful result and subresult response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC825 responses when SOAPAction is missing or invalid
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2931", "User Story")
@scenario("Compare SC825 responses when SOAPAction is missing or invalid")
def test_compare_sc825_responses_when_soap_action_is_missing_or_invalid():
    """Compare SC825 responses when SOAPAction is missing or invalid"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC825 responses when the client or user cannot be validated
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2931", "User Story")
@scenario("Compare SC825 responses when the client or user cannot be validated")
def test_compare_sc825_responses_when_client_or_user_cannot_be_validated():
    """Compare SC825 responses when the client or user cannot be validated"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Compare LDAP exception response when security details are missing or invalid
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2931", "User Story")
@scenario("Compare SC825 LDAP exception response when security details are missing or invalid")
def test_compare_sc825_ldap_exception_response_when_security_details_are_missing_or_invalid():
    """Compare SC825 LDAP exception response when security details are missing or invalid"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc825_payload_setup()


@given(parsers.parse("I create the correct api payload for {client_type}"), target_fixture="payload")
def create_correct_payload_for_client_type(client_type):
    return sc825_payload_setup(client_type)


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    return sc825_payload_setup(conditions)


@given(parsers.parse("I create the api payload for {condition}"), target_fixture="payload")
def create_business_error_payload(condition):
    return sc825_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send inquire participant request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC825", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send the inquire participant request to Azure endpoint", target_fixture="response_azure")
@when("I send inquire participant request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC825", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC825")
def then_i_can_see_all_the_responses_are_identical_for_sc825(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC825", ignore_element_order=True)
