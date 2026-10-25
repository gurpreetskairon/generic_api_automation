# William: Skipped this test file because it was an async service
# import allure
# from pytest_bdd import given, parsers, then
#
# from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
# from utils.api_utils.helper.payload_setup import sc809_payload_setup
# from utils.bdd_utils.scenario import scenario
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC809 successful transaction response
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4280", "API-4280")
# @scenario("Compare SC809 successful transaction response")
# def test_compare_sc809_successful_transaction_response():
#     """Compare SC809 successful transaction response."""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 2 - Compare SC809 unsuccessful transaction response
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4280", "API-4280")
# @scenario("Compare SC809 unsuccessful transaction response")
# def test_compare_sc809_unsuccessful_transaction_response():
#     """Compare SC809 unsuccessful transaction response."""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Given steps
# # ══════════════════════════════════════════════════════════════════════════════
# @given(parsers.parse("I create the correct SC809 api payload with different {conditions}"), target_fixture="payload")
# def create_sc809_payload_with_condition(conditions):
#     return sc809_payload_setup(conditions)
#
#
# @given("I send the SC809 request to IIB endpoint", target_fixture="response_iib")
# def send_sc809_request_to_iib_endpoint(api_client, payload):
#     endpoint = build_api_endpoint("SC809", system="IIB")
#
#     return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])
#
#
# @given("I send the SC809 request to Azure endpoint", target_fixture="response_azure")
# def send_sc809_request_to_azure_endpoint(api_client, payload):
#     endpoint = build_api_endpoint("SC809", system="AZURE")
#
#     headers = payload["header"].copy()
#     headers["MSD-Sub-Env"] = "d11"
#
#     return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=headers)
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Then steps
# # ══════════════════════════════════════════════════════════════════════════════
# @then("I can see all the responses are identical for SC809")
# def compare_all_sc809_responses(api_client, response_iib, response_azure):
#     api_client.compare_soap_responses(response_iib, response_azure, "SC809")
