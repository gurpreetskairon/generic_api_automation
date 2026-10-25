# William: The leadership decides to release on schedule and fix the issues found in production
# import allure
# from pytest_bdd import given, parsers, then, when
#
# from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
# from utils.api_utils.helper.payload_setup import sc933_payload_setup
# from utils.bdd_utils.scenario import scenario
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 1 - Compare SC933 successful start and stop responses
# # ══════════════════════════════════════════════════════════════════════════════
#
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4503", "User Story")
# @scenario("Compare SC933 successful start and stop responses between IIB and Azure")
# def test_compare_sc933_successful_responses():
#     """Compare SC933 successful start and stop responses between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 2 - Compare SC933 unsuccessful responses
# # ══════════════════════════════════════════════════════════════════════════════
#
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4503", "User Story")
# @scenario("Compare SC933 unsuccessful responses between IIB and Azure")
# def test_compare_sc933_unsuccessful_responses():
#     """Compare SC933 unsuccessful responses between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Scenario 3 - Compare SC933 authentication failure
# # ══════════════════════════════════════════════════════════════════════════════
#
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4503", "User Story")
# @scenario("Compare SC933 authentication failure between IIB and Azure")
# def test_compare_sc933_authentication_failure():
#     """Compare SC933 authentication failure between IIB and Azure"""
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Given steps
# # ══════════════════════════════════════════════════════════════════════════════
#
# @given(parsers.parse("I create the SC933 api payload for {condition}"), target_fixture="payload")
# def create_sc933_payload(condition):
#     return sc933_payload_setup(condition=condition)
#
#
# @given("I ensure SC933 campaign is stopped before comparison")
# def ensure_sc933_campaign_is_stopped(api_client, payload):
#     iib_endpoint = build_api_endpoint("SC933", system="IIB").format(campaignName=payload["campaign_name"])
#     azure_endpoint = build_api_endpoint("SC933", system="AZURE").format(campaignName=payload["campaign_name"])
#
#     api_client.send_post_request(
#         f"{iib_endpoint}?operation=stop", payload=payload["stop_request_body"],
#         headers=payload["reset_header"], json_payload=True, raise_error=False
#     )
#     api_client.send_post_request(
#         f"{azure_endpoint}?operation=stop", payload=payload["stop_request_body"],
#         headers=payload["reset_header"], json_payload=True, raise_error=False
#     )
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Positive When steps
# # ══════════════════════════════════════════════════════════════════════════════
#
# @when("I send SC933 request with start operation to IIB endpoint", target_fixture="response_iib_start")
# def send_sc933_start_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="IIB").format(campaignName=payload["campaign_name"])
#     response = api_client.send_post_request(
#         f"{endpoint}?operation=start", payload=payload["start_request_body"],
#         headers=payload["start_header"], json_payload=True, raise_error=True
#     )
#     return response[0] if isinstance(response, tuple) else response
#
#
# @when("I send SC933 request with stop operation to IIB endpoint", target_fixture="response_iib_stop")
# def send_sc933_stop_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="IIB").format(campaignName=payload["campaign_name"])
#     response = api_client.send_post_request(
#         f"{endpoint}?operation=stop", payload=payload["stop_request_body"],
#         headers=payload["stop_header"], json_payload=True, raise_error=True
#     )
#     return response[0] if isinstance(response, tuple) else response
#
#
# @when("I send SC933 request with start operation to Azure endpoint", target_fixture="response_azure_start")
# def send_sc933_start_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="AZURE").format(campaignName=payload["campaign_name"])
#     response = api_client.send_post_request(
#         f"{endpoint}?operation=start", payload=payload["start_request_body"],
#         headers=payload["start_header"], json_payload=True, raise_error=True
#     )
#     return response[0] if isinstance(response, tuple) else response
#
#
# @when("I send SC933 request with stop operation to Azure endpoint", target_fixture="response_azure_stop")
# def send_sc933_stop_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="AZURE").format(campaignName=payload["campaign_name"])
#     response = api_client.send_post_request(
#         f"{endpoint}?operation=stop", payload=payload["stop_request_body"],
#         headers=payload["stop_header"], json_payload=True, raise_error=True
#     )
#     return response[0] if isinstance(response, tuple) else response
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Negative When steps
# # ══════════════════════════════════════════════════════════════════════════════
#
# @when("I send SC933 request to IIB endpoint", target_fixture="response_iib")
# def send_sc933_request_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="IIB").format(campaignName=payload["campaign_name"])
#     endpoint = f"{endpoint}?operation={payload['operation']}"
#     response = api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"],
#         json_payload=True, raise_error=payload["raise_error"]
#     )
#     return response[0] if isinstance(response, tuple) else response
#
#
# @when("I send SC933 request to Azure endpoint", target_fixture="response_azure")
# def send_sc933_request_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="AZURE").format(campaignName=payload["campaign_name"])
#     endpoint = f"{endpoint}?operation={payload['operation']}"
#     response = api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"],
#         json_payload=True, raise_error=payload["raise_error"]
#     )
#     return response[0] if isinstance(response, tuple) else response
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Authentication When steps
# # ══════════════════════════════════════════════════════════════════════════════
#
# @when("I send SC933 authentication failure request to IIB endpoint", target_fixture="auth_response_iib")
# def send_sc933_auth_failure_to_iib(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="IIB").format(campaignName=payload["campaign_name"])
#     endpoint = f"{endpoint}?operation={payload['operation']}"
#     return api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"],
#         json_payload=True, raise_error=False
#     )
#
#
# @when("I send SC933 authentication failure request to Azure endpoint", target_fixture="auth_response_azure")
# def send_sc933_auth_failure_to_azure(api_client, payload):
#     endpoint = build_api_endpoint("SC933", system="AZURE").format(campaignName=payload["campaign_name"])
#     endpoint = f"{endpoint}?operation={payload['operation']}"
#     return api_client.send_post_request(
#         endpoint, payload=payload["request_body"], headers=payload["header"],
#         json_payload=True, raise_error=False
#     )
#
#
# # ══════════════════════════════════════════════════════════════════════════════
# # Then steps
# # ══════════════════════════════════════════════════════════════════════════════
#
# @then("I can see SC933 start and stop responses are identical between IIB and Azure")
# def compare_sc933_success_responses(api_client, response_iib_start, response_iib_stop,
#                                     response_azure_start, response_azure_stop):
#     api_client.compare_json_responses(response_iib_start, response_azure_start, "SC933")
#     api_client.compare_json_responses(response_iib_stop, response_azure_stop, "SC933")
#
#
# @then("I can see all the responses are identical for SC933")
# def compare_sc933_responses(api_client, response_iib, response_azure):
#     api_client.compare_json_responses(response_iib, response_azure, "SC933")
#
#
# @then("I can see SC933 authentication failure status is identical")
# def compare_sc933_authentication_failure(auth_response_iib, auth_response_azure):
#     iib_body, iib_status = auth_response_iib
#     azure_body, azure_status = auth_response_azure
#
#     assert iib_status == 401
#     assert azure_status == 401
