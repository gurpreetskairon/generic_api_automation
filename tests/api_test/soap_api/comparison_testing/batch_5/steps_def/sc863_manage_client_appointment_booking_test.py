import allure
from pytest_bdd import given, parsers, then, when
from apps.services.integration_soap.payload_data.sc863 import update_sc863_endpoint, update_sc863_db_table_values
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc863_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC863 successful responses
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare SC863 successful responses between IIB and Azure")
def test_compare_sc863_successful_responses():
    """Compare SC863 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC863 delete appointment negative responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare SC863 delete appointment negative responses between IIB and Azure")
def test_compare_sc863_delete_appointment_responses():
    """Compare SC863 delete appointment negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC863 book appointment negative responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare SC863 book appointment negative responses between IIB and Azure")
def test_compare_sc863_book_appointment_responses():
    """Compare SC863 book appointment negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC863 reschedule appointment negative responses between IIB and Azure
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare SC863 reschedule appointment negative responses between IIB and Azure")
def test_compare_sc863_reschedule_appointment_responses():
    """Compare SC863 reschedule appointment negative responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Compare SC863 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-API-4129", "User Story")
@scenario("Compare SC863 http exception responses")
def test_compare_sc863_http_exception_responses():
    """Compare SC863 http exception responses"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC863 api {request} payload for {condition}"), target_fixture="payload")
def create_sc863_payload(request, condition):
    azure_payload = sc863_payload_setup(condition=condition, request_type=request), request, condition
    iib_payload = sc863_payload_setup(condition=condition, request_type=request), request, condition
    return iib_payload, azure_payload


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC863 request to IIB endpoint", target_fixture="response_iib")
def send_sc863_request_to_iib(api_client, payload):
    if payload[0][1] == "cancel_appointment":
        endpoint = build_api_endpoint("SC863_CANCEL", system="IIB")
        endpoint, params = update_sc863_endpoint(endpoint, f"{payload[0][1]}_IIB", payload[0][2])
        return api_client.send_delete_request(endpoint, params=params, headers=payload[0][0][0], raise_on_error=False)
    else:
        endpoint = build_api_endpoint("SC863_NEW_RESCHEDULE", system="IIB")
        endpoint = update_sc863_endpoint(endpoint, f"{payload[0][1]}_IIB", payload[0][2])
        if endpoint[1] is not None:
            response = api_client.send_post_request(
                endpoint[0],
                payload=payload[0][0][1],
                headers=payload[0][0][0],
                json_payload=True,
                raise_error=False,
                params=endpoint[1]
            )
        else:
            response = api_client.send_post_request(
                endpoint[0], payload=payload[0][0][1], headers=payload[0][0][0], json_payload=True, raise_error=False
            )
        if payload[0][2] not in [
            "invalid_request",
            "timeslot_not_available_preferred_office",
            "timeslot_not_available_with_staff_member",
            "error_404_uri_not_recognised",
            "error_401_client_auth_failed",
            "error_500_server_exception",
        ]:
            try:
                update_sc863_db_table_values(response[0])
            except Exception as e:
                allure.attach(response[0], name="IIB Request Failure", attachment_type=allure.attachment_type.JSON)
                raise Exception(f"Failed to update SC863 table values:{e}..... IIB API response was {response[0]}")
        return response


@when("I send SC863 request to Azure endpoint", target_fixture="response_azure")
def send_sc863_request_to_azure(api_client, payload):
    if payload[1][1] == "cancel_appointment":
        endpoint = build_api_endpoint("SC863_CANCEL", system="AZURE")
        endpoint, params = update_sc863_endpoint(endpoint, f"{payload[1][1]}_AZURE", payload[1][2])
        return api_client.send_delete_request(endpoint, params=params, headers=payload[1][0][0], raise_on_error=False)
    else:
        endpoint = build_api_endpoint("SC863_NEW_RESCHEDULE", system="AZURE")
        endpoint = update_sc863_endpoint(endpoint, f"{payload[1][1]}_AZURE", payload[1][2])
        if endpoint[1] is not None:
            response = api_client.send_post_request(endpoint[0], payload=payload[1][0][1], headers=payload[1][0][0],
                                                    json_payload=True, raise_error=False, params=endpoint[1])
        else:
            response = api_client.send_post_request(endpoint[0], payload=payload[1][0][1], headers=payload[1][0][0],
                                                    json_payload=True, raise_error=False)

        if payload[1][2] not in [
            "invalid_request",
            "timeslot_not_available_preferred_office",
            "timeslot_not_available_with_staff_member",
            "error_404_uri_not_recognised",
            "error_401_client_auth_failed",
            "error_500_server_exception",
        ]:
            try:
                update_sc863_db_table_values(response[0], "AZURE")
            except Exception as e:
                allure.attach(response[0], name="AZURE Request Failure", attachment_type=allure.attachment_type.JSON)
                raise Exception(f"Failed to update SC863 table values:{e}..... Azure API response was {response[0]}")
        return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC863")
def compare_sc863_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "SC863", exclude_fields=["addDateTime", "id",
                                                                                             "identifier", "familyName",
                                                                                             "firstName", "fullName",
                                                                                             "endDate", "startDate"])

@then("I can see the error responses are identical for SC863")
def compare_sc863_error_responses(api_client, response_iib, response_azure):
    api_client.compare_status_code(response_iib[1], response_azure[1])

