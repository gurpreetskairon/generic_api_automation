import json
import os
from datetime import datetime

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from default_config import JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario


@scenario("Check the status of employer profile")
def test_check_the_status_of_employer_profile():
    pass


@given(parsers.parse("I send a request with {status}"))
def build_and_send_request(api_request_detail_obj: ApiRequestDetails, status):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "employer_profile_endpoint",
    )

    directory = os.path.dirname(__file__)
    expected_data_path = os.path.join(directory, "jsons", "employer_profile.json")
    with open(expected_data_path, "r") as file:
        api_request_detail_obj.body_data = json.load(file)

    if status == "Accepted":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY,
            "transactionId": f"EmployerProfile{status}_AutoTest",
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceSystem": "CMS",
            "sourceEventType": "CREATE",
        }
    elif status == "Source header":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY,
            "transactionId": f"EmployerProfile{status}_AutoTest",
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceSystem": "CMS",
        }
    elif status == "Bad Request":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY,
            "transactionId": f"EmployerProfile{status}_AutoTest",
            "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventType": "UPDATE",
        }
    elif status == "Unauthorized":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": f"test-{JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY}",
            "transactionId": f"EmployerProfile{status}_AutoTest",
            "sourceSystem": "CMS",
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventType": "CREATE",
        }
    elif status == "Empty payload":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY,
            "transactionId": f"EmployerProfile{status}_AutoTest",
            "sourceSystem": "CMS",
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventType": "CREATE",
        }
        api_request_detail_obj.body_data = None
    elif status == "Method Not Allowed":
        api_request_detail_obj.headers = {
            "transactionId": f"EmployerProfile{status}_AutoTest",
            "sourceSystem": "CMS",
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventType": "CREATE",
        }
    elif status == "Resource Not Found":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY,
            "transactionId": f"EmployerProfile{status}_AutoTest",
            "sourceSystem": "CMS",
            "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "Content-Type": "application/json",
            "sourceEventType": "CREATE",
        }
        api_request_detail_obj.endpoint = f"{api_request_detail_obj.endpoint}123"

    if status == "Method Not Allowed":
        api_request_detail_obj.send_put_request()
    else:
        api_request_detail_obj.send_post_request()


@then(
    parsers.parse(
        "I can see status {codes} in the response and the response body should match the " "expected {expected_result}"
    )
)
def validate_response(api_request_detail_obj: ApiRequestDetails, codes, expected_result):
    api_request_detail_obj.verify_status_code(int(codes))
    if expected_result != "none":
        # Construct the expected_result file path dynamically
        directory = os.path.dirname(__file__)
        filename = str(expected_result)
        expected_data_path = os.path.join(
            directory,
            "jsons",
            "expected_responses",
            "employer_profile",
            filename + ".json",
        )
        api_request_detail_obj.verify_response_from_file(expected_data_path)
