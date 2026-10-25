from types import SimpleNamespace

import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.payload_setup import build_api_endpoint, dp830_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare successful response when client has program tags and client flags
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3629", "User Story")
@scenario("Compare DP830 successful response when client has programme tags and client flags")
def test_compare_dp830_successful_response_when_client_has_programme_tags_and_client_flags():
    """Compare DP830 successful response when client has programme tags and client flags"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP830 successful result
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3629", "User Story")
@scenario("Compare DP830 successful result")
def test_compare_dp830_successful_result():
    """Compare DP830 successful result"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare DP830 responses when the client or user cannot be validated
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3629", "User Story")
@scenario("Compare DP830 responses when the client or user cannot be validated")
def test_compare_dp830_responses_when_the_client_or_user_cannot_be_validated():
    """Compare DP830 responses when the client or user cannot be validated"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    return dp830_payload_setup()


@given(parsers.parse("I create the correct api payload for {client_type}"), target_fixture="payload")
def create_correct_payload_for_client_type(client_type):
    return dp830_payload_setup(client_type)


@given(parsers.parse("I create the api payload for {condition}"), target_fixture="payload")
def create_payload_for_condition(condition):
    return dp830_payload_setup(condition)


@given("I send inquire participant request for client tags and flags to IIB endpoint", target_fixture="iib_response")
def send_inquire_participant_request_for_client_tags_and_flags_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP830", system="IIB", sub_system="MYMSD")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1], raise_on_error=False)


@given(
    "I send inquire participant request for client tags and flags to Azure endpoint", target_fixture="azure_response"
)
def send_inquire_participant_request_for_client_tags_and_flags_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP830", system="AZURE")
    return api_client.send_get_request(endpoint, headers=payload[0], params=payload[1], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, iib_response, azure_response):
    api_client.compare_json_responses(iib_response[0], azure_response[0], "DP830", exclude_fields=["requestDateTime"])
