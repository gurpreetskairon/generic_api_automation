import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc531_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Successful JSS reapplication
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3621", "User Story")
@scenario("Compare SC531 successful JSS reapplication responses")
def test_compare_sc531_successful_jss_reapplication_responses():
    """Compare SC531 successful JSS reapplication responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Unsuccessful JSS reapplication
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3621", "User Story")
@scenario("Compare SC531 unsuccessful JSS reapplication responses")
def test_compare_sc531_unsuccessful_jss_reapplication_responses():
    """Compare SC531 unsuccessful JSS reapplication responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Unrecognised user
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3621", "User Story")
@scenario("Compare SC531 response for an unrecognised user")
def test_compare_sc531_unrecognised_user_response():
    """Compare SC531 response for an unrecognised user"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Unrecognised client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3621", "User Story")
@scenario("Compare SC531 response for an unrecognised client")
def test_compare_sc531_unrecognised_client_response():
    """Compare SC531 response for an unrecognised client"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Client not eligible for reassessment
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3621", "User Story")
@scenario("Compare SC531 response when the client is not eligible for reassessment")
def test_compare_sc531_client_not_eligible_for_reassessment():
    """Compare SC531 client not eligible for reassessment response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the api payload for {condition}"), target_fixture="payload")
def create_sc531_payload(condition):
    return sc531_payload_setup(condition=condition)


@given("I send establish entitlement request to IIB endpoint", target_fixture="response_iib")
def send_sc531_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC531", system="IIB")
    return api_client.send_post_request(
        endpoint, payload=payload["iib_request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


@given("I send establish entitlement request to Azure endpoint", target_fixture="response_azure")
def send_sc531_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC531", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=payload["azure_request_body"], headers=payload["header"], raise_error=payload["raise_error"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the SC531 responses are identical")
def compare_sc531_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(
        response_iib, response_azure, "SC531", ignore_element_order=True, ignore_tags=["objectId"]
    )
