# William: The leadership decides to release on schedule and fix the issues found in production
# import allure
# from pytest_bdd import given, parsers, then
#
# from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
# from utils.api_utils.helper.payload_setup import sc935_payload_setup
# from utils.bdd_utils.scenario import scenario
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC935 successful transaction response
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4505", "API-4505")
# @scenario("Compare SC935 successful transaction response")
# def test_compare_sc935_successful_transaction_response():
#     """Compare SC935 successful transaction response."""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 2 - Compare SC935 unsuccessful transaction response
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4505", "API-4505")
# @scenario("Compare SC935 unsuccessful transaction response")
# def test_compare_sc935_unsuccessful_transaction_response():
#     """Compare SC935 unsuccessful transaction response."""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Given steps
# # ══════════════════════════════════════════════════════════════════════════════
# @given(parsers.parse("I create the correct SC935 api request with different {conditions}"), target_fixture="payload")
# def create_sc935_request_with_condition(conditions):
#     return sc935_payload_setup(conditions)
#
#
# @given("I send the SC935 request to IIB endpoint", target_fixture="response_iib")
# def send_sc935_request_to_iib_endpoint(api_client, payload):
#     endpoint = build_api_endpoint("SC935", system="IIB").replace("{campaignName}", payload["campaign_name"])
#     return api_client.send_get_request(endpoint, headers=payload["header"], raise_on_error=payload["raise_on_error"])
#
#
# @given("I send the SC935 request to Azure endpoint", target_fixture="response_azure")
# def send_sc935_request_to_azure_endpoint(api_client, payload):
#     endpoint = build_api_endpoint("SC935", system="AZURE").replace("{campaignName}", payload["campaign_name"])
#     return api_client.send_get_request(endpoint, headers=payload["header"], raise_on_error=payload["raise_on_error"])
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Then steps
# # ══════════════════════════════════════════════════════════════════════════════
# @then("I can see all the responses are identical for SC935")
# def compare_all_sc935_responses(api_client, response_iib, response_azure):
#     api_client.compare_json_responses(response_iib, response_azure, "SC935")
