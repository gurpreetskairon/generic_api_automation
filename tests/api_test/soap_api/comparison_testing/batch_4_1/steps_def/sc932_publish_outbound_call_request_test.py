# William: The leadership decides to release on schedule and fix the issues found in production
# import allure
# from pytest_bdd import given, parsers, then, when
#
# from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
# from utils.api_utils.helper.payload_setup import sc932_payload_setup
# from utils.bdd_utils.scenario import scenario
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC932 successful responses between IIB and Azure
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4502", "User Story")
# @scenario("Compare SC932 successful responses between IIB and Azure")
# def test_compare_sc932_successful_responses():
#     """Compare SC932 successful responses between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 2 - Compare SC932 unsuccessful responses between IIB and Azure
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4502", "User Story")
# @scenario("Compare SC932 unsuccessful responses between IIB and Azure")
# def test_compare_sc932_unsuccessful_responses():
#     """Compare SC932 unsuccessful responses between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 3 - Compare SC932 exception responses between IIB and Azure
# # ══════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4502", "User Story")
# @scenario("Compare SC932 authentication failure between IIB and Azure")
# def test_compare_sc932_authentication_failure():
#     """Compare SC932 authentication failure between IIB and Azure"""
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Given steps
# # ══════════════════════════════════════════════════════════════════════════════
# @given(parsers.parse("I create the SC932 api payload for {condition}"), target_fixture="payload")
# def create_sc932_payload(condition):
#     return sc932_payload_setup(condition=condition)
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # When steps
# # ══════════════════════════════════════════════════════════════════════════════
# @when("I send SC932 request to IIB endpoint", target_fixture="response_iib")
# def send_sc932_request_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC932", system="IIB").format(
#         callingList=payload["calling_list"], clientId=payload["client_id"]
#     )
#     return api_client.send_post_request(
#         endpoint,
#         payload=payload["request_body"],
#         headers=payload["header"],
#         json_payload=True,
#         raise_error=payload["raise_error"]
#     )
#
#
# @when("I send SC932 request to Azure endpoint", target_fixture="response_azure")
# def send_sc932_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC932", system="AZURE").format(
#         callingList=payload["calling_list"], clientId=payload["client_id"]
#     )
#     return api_client.send_post_request(
#         endpoint,
#         payload=payload["request_body"],
#         headers=payload["header"],
#         json_payload=True,
#         raise_error=payload["raise_error"]
#     )
#
#
# @when("I send SC932 authentication failure request to IIB endpoint", target_fixture="auth_response_iib")
# def send_sc932_auth_failure_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC932", system="IIB").format(
#         callingList=payload["calling_list"], clientId=payload["client_id"]
#     )
#     return api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"], json_payload=True, raise_error=False
#     )
#
#
# @when("I send SC932 authentication failure request to Azure endpoint", target_fixture="auth_response_azure")
# def send_sc932_auth_failure_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC932", system="AZURE").format(
#         callingList=payload["calling_list"], clientId=payload["client_id"]
#     )
#     return api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"], json_payload=True, raise_error=False
#     )
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Then steps
# # ══════════════════════════════════════════════════════════════════════════════
# @then("I can see all the responses are identical for SC932")
# def compare_sc932_responses(api_client, response_iib, response_azure):
#     api_client.compare_json_responses(response_iib, response_azure, "SC932")
#
#
# @then("I can see SC932 authentication failure status is identical")
# def compare_sc932_authentication_failure(auth_response_iib, auth_response_azure):
#     iib_body, iib_status = auth_response_iib
#     azure_body, azure_status = auth_response_azure
#     assert iib_status == 401
#     assert azure_status == 401
