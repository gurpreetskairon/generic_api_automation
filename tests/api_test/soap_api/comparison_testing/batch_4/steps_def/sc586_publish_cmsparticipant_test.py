import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc586_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC586 successful responses between IIB and Azure for adding and editing a child record
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3936", "User Story")
@scenario("Compare SC586 successful responses between IIB and Azure for adding and editing a child record")
def test_compare_sc586_successful_responses_for_adding_editing_child():
    """Compare SC586 successful responses between IIB and Azure for adding and editing a child record"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC586 successful responses between IIB and Azure for adding and editing a client record
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3936", "User Story")
@scenario("Compare SC586 successful responses between IIB and Azure for adding and editing a client record")
def test_compare_sc586_successful_responses_for_adding_editing_client():
    """Compare SC586 successful responses between IIB and Azure for adding and editing a client record"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC586 successful responses between IIB and Azure for negative scenarios
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3936", "User Story")
@scenario("Compare SC586 successful responses between IIB and Azure for negative scenarios")
def test_compare_sc586_successful_responses_for_negative_scenarios():
    """Compare SC586 successful responses between IIB and Azure for negative scenarios"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC586 api {payload} payload for {condition}"), target_fixture="payload")
def create_sc586_payload(condition, payload):
    return sc586_payload_setup(condition=condition, payload_type=payload)


# ══════════════════════════════════════════════════════════════════════════════════════
# When Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC586 request to IIB endpoint", target_fixture="response_iib")
def send_sc586_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC586", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


@when("I send SC586 request to Azure endpoint", target_fixture="response_azure")
def send_sc586_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC586", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then Steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC586")
def compare_sc586_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC586", ignore_element_order=True)
