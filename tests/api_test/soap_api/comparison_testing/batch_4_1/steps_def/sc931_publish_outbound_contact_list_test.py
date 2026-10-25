# William: The leadership decides to release on schedule and fix the issues found in production
# import json
#
# import allure
# from pytest_bdd import given, parsers, then, when
# from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
# from utils.api_utils.helper.payload_setup import sc931_payload_setup
# from utils.bdd_utils.scenario import scenario
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC931 successful response for publishing a new request between IIB and Azure
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4170", "User Story")
# @scenario("Compare SC931 successful response for publishing a new request between IIB and Azure")
# def test_compare_sc931_successful_responses_for_new_request():
#     """Compare SC931 successful response for publishing a new request between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 2 - Compare SC931 successful responses for altering a existing request between IIB and Azure
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4170", "User Story")
# @scenario("Compare SC931 successful responses for altering a existing Contact list between IIB and Azure")
# def test_compare_sc931_successful_responses_for_existing_request():
#     """Compare SC931 successful responses for altering a existing Contact list between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 3 - Compare SC931 unsuccessful responses between IIB and Azure
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4170", "User Story")
# @scenario("Compare SC931 unsuccessful responses between IIB and Azure")
# def test_compare_sc931_unsuccessful_responses():
#     """Compare SC931 unsuccessful responses between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 4 - Compare SC931 exception responses between IIB and Azure
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4170", "User Story")
# @scenario("Compare SC931 exception responses between IIB and Azure")
# def test_compare_sc931_exception_responses():
#     """Compare SC931 exception responses between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Given steps
# # ══════════════════════════════════════════════════════════════════════════════
# @given(parsers.parse("I create the SC931 api payload for {condition}"), target_fixture="payload")
# def create_sc931_payload(condition):
#     return sc931_payload_setup(condition)
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # When steps
# # ══════════════════════════════════════════════════════════════════════════════
# @when("I send SC931 request to IIB endpoint", target_fixture="response_iib")
# def send_sc931_request_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC931", system="IIB")
#     if payload[1]["action"] == "update" or payload[1]["action"] == "cancelrecord":
#         return api_client.send_put_request(endpoint, payload=json.dumps(payload[1]), headers=payload[0])
#     else:
#         return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0], json_payload=True)
#
#
#
# @when("I send SC931 request to Azure endpoint", target_fixture="response_azure")
# def send_sc931_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC931", system="AZURE")
#     if payload[1]["action"] == "update" or payload[1]["action"] == "cancel":
#         return api_client.send_put_request(endpoint, payload=json.dumps(payload[1]), headers=payload[0])
#     else:
#         return api_client.send_post_request(endpoint, payload=payload[1], headers=payload[0], json_payload=True)
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Then steps
# # ══════════════════════════════════════════════════════════════════════════════
# @then("I can see all the responses are identical for SC931")
# def compare_sc931_responses(api_client, response_iib, response_azure):
#     if type(response_iib) == tuple:
#         api_client.compare_json_responses(response_iib, response_azure, "SC931")
#     else:
#         api_client.compare_error_strings(response_iib, response_azure, "SC931")
#
#
