# William: The leadership decides to release on schedule and fix the issues found in production
# import allure
# from pytest_bdd import given, parsers, then
#
# from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
# from utils.api_utils.helper.payload_setup import sc934_payload_setup
# from utils.bdd_utils.scenario import scenario
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC934 successful transaction response
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4504", "API-4504")
# @scenario("Compare SC934 successful transaction response")
# def test_compare_sc934_successful_transaction_response():
#     """Compare SC934 successful transaction response."""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 2 - Compare SC934 invalid request response
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4504", "API-4504")
# @scenario("Compare SC934 invalid request response")
# def test_compare_sc934_invalid_request_response():
#     """Compare SC934 invalid request response."""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Given steps
# # ══════════════════════════════════════════════════════════════════════════════
# @given(parsers.parse("I create the correct SC934 api request with different {conditions}"), target_fixture="payload")
# def create_sc934_request_with_condition(conditions):
#     return sc934_payload_setup(conditions)
#
#
# @given(
#     "I send the SC934 request to IIB endpoint",
#     target_fixture="response_iib",
# )
# def send_sc934_request_to_iib_endpoint(api_client, payload):
#     endpoint = build_api_endpoint("SC934", system="IIB")
#     endpoint = endpoint.replace(
#         "{campaignName}",
#         payload["campaign_name"],
#     )
#
#     return api_client.send_get_request(
#         endpoint,
#         headers=payload["header"],
#         raise_on_error=False,
#     )
#
#
# @given(
#     "I send the SC934 request to Azure endpoint",
#     target_fixture="response_azure",
# )
# def send_sc934_request_to_azure_endpoint(api_client, payload):
#     endpoint = build_api_endpoint("SC934", system="AZURE")
#     endpoint = endpoint.replace(
#         "{campaignName}",
#         payload["campaign_name"],
#     )
#
#     return api_client.send_get_request(
#         endpoint,
#         headers=payload["header"],
#         raise_on_error=False,
#     )
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Then step
# # ══════════════════════════════════════════════════════════════════════════════
# @then("I can see all the responses are identical for SC934")
# def compare_all_sc934_responses(api_client, response_iib, response_azure):
#     api_client.compare_json_responses(response_iib, response_azure, "SC934")
