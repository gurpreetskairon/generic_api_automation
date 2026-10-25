import allure
from pytest_bdd import given, parsers, then, when
from apps.services.integration_soap.payload_data.dp863 import update_dp863_endpoint, update_dp863_db_table_values
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc863_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP863 successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare DP863 successful responses between IIB and Azure")
def test_compare_dp863_successful_responses():
    """Compare DP863 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP863 delete appointment negative responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare DP863 delete appointment negative responses between IIB and Azure")
def test_compare_dp863_delete_appointment_responses():
    """Compare DP863 delete appointment negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare DP863 book appointment negative responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare DP863 book appointment negative responses between IIB and Azure")
def test_compare_dp863_book_appointment_responses():
    """Compare DP863 book appointment negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare DP863 reschedule appointment negative responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare DP863 reschedule appointment negative responses between IIB and Azure")
def test_compare_dp863_reschedule_appointment_responses():
    """Compare DP863 reschedule appointment negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Compare DP863 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare DP863 http exception responses")
def test_compare_dp863_http_exception_responses():
    """Compare DP863 http exception responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the DP863 api {request} payload for {condition}"), target_fixture="payload")
def create_dp863_payload(request, condition):
    return sc863_payload_setup(condition=condition, request_type=request), request, condition


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send DP863 request to IIB endpoint", target_fixture="response_iib")
def send_dp863_request_to_iib(api_client, payload):
    if payload[1] == "cancel_appointment":
        endpoint = build_api_endpoint("DP863_CANCEL", system="IIB")
        endpoint, params = update_dp863_endpoint(endpoint, payload[1], payload[2])
        return api_client.send_delete_request(endpoint, params=params, headers=payload[0][0], raise_on_error=False)
    else:
        endpoint = build_api_endpoint("DP863_NEW_RESCHEDULE", system="IIB")
        endpoint = update_dp863_endpoint(endpoint, payload[1], payload[2])
        if endpoint[1] is not None:
            response = api_client.send_post_request(
                endpoint[0],
                payload=payload[0][1],
                headers=payload[0][0],
                json_payload=True,
                raise_error=False,
                params=endpoint[1]
            )
        else:
            response = api_client.send_post_request(
                endpoint[0], payload=payload[0][1], headers=payload[0][0], json_payload=True, raise_error=False
            )
        if payload[2] not in [
            "invalid_request",
            "timeslot_not_available_preferred_office",
            "timeslot_not_available_with_staff_member",
            "error_404_uri_not_recognised",
            "error_401_client_auth_failed",
            "error_500_server_exception",
        ]:
            update_dp863_db_table_values(response[0])
        return response


@when("I send DP863 request to Azure endpoint", target_fixture="response_azure")
def send_dp863_request_to_azure(api_client, payload):
    if payload[1] == "cancel_appointment":
        endpoint = build_api_endpoint("DP863_CANCEL", system="AZURE")
        endpoint, params = update_dp863_endpoint(endpoint, payload[1], payload[2])
        return api_client.send_delete_request(endpoint, params=params, headers=payload[0][0], raise_on_error=False)
    else:
        endpoint = build_api_endpoint("DP863_NEW_RESCHEDULE", system="AZURE")
        endpoint = update_dp863_endpoint(endpoint, payload[1], payload[2])
        response = api_client.send_post_request(
            endpoint, payload=payload[0][1], headers=payload[0][0], json_payload=True, raise_error=False
        )
        return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP863")
def compare_dp863_responses(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "DP863", ignore_element_order=True)
