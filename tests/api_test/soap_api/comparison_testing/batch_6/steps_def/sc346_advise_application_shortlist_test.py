# William: Skipped this test file because it was an async service
# import allure
# from pytest_bdd import given, parsers, then, when
#
# from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
# from utils.api_utils.helper.payload_setup import sc346_payload_setup
# from utils.bdd_utils.scenario import scenario
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC346 successful transaction response
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4525", "User Story")
# @scenario("Compare SC346 successful transaction response")
# def test_compare_sc346_successful_transaction_response():
#     """Compare SC346 successful transaction response."""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Given steps
# # ══════════════════════════════════════════════════════════════════════════════
# @given(parsers.parse("I create the correct SC346 api payload with different {conditions}"), target_fixture="payload")
# def create_sc346_payload_with_condition(conditions):
#     return sc346_payload_setup(condition=conditions)
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # When steps
# # ══════════════════════════════════════════════════════════════════════════════
# @when("I send the SC346 request to IIB endpoint", target_fixture="response_iib")
# def send_sc346_request_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC346", system="IIB")
#
#     response = api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=False
#     )
#     return response
#
#
# @when("I send the SC346 request to Azure endpoint", target_fixture="response_azure")
# def send_sc346_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC346", system="AZURE")
#
#     return api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"], raise_error=payload["raise_error"]
#     )
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Then steps
# # ══════════════════════════════════════════════════════════════════════════════
# @then("I can see all the responses are identical for SC346")
# def compare_sc346_responses(api_client, response_iib, response_azure):
#     api_client.compare_soap_responses(response_iib, response_azure, "SC346", ignore_element_order=True)
