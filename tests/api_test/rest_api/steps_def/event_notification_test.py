import json
import os

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from default_config import EVENT_NOTIFICATIONS_APIM_SUBSCRIPTION_KEY
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario
from utils.common_utils.helper_functions.json_parser import open_json_file


@scenario("Check the status of event notifications")
def test_check_the_status_of_event_notifications():
    pass


@given(parsers.parse("I send a request with {status}"))
def build_and_send_request(api_request_detail_obj: ApiRequestDetails, status):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "event_notification_endpoint",
    )

    api_request_detail_obj.headers = {
        "apimSubscriptionKey": EVENT_NOTIFICATIONS_APIM_SUBSCRIPTION_KEY,
        "transactionId": f"EventNotification{status}_AutoTest",
        "Content-Type": "application/cloudevents+json",
        "Ocp-Apim-Trace": "true",
    }

    directory = os.path.dirname(__file__)
    expected_data_path = os.path.join(directory, "jsons", "event_notifications.json")
    api_request_detail_obj.body_data = open_json_file(expected_data_path, "r")

    if status == "bad request":
        api_request_detail_obj.body_data["id"] = "A1234201"
        del api_request_detail_obj.headers["transactionId"]
        del api_request_detail_obj.headers["Ocp-Apim-Trace"]
    elif status == "Internal Server Error":
        api_request_detail_obj.body_data = None
        del api_request_detail_obj.headers["Ocp-Apim-Trace"]
    elif status == "validate handshake":
        del api_request_detail_obj.headers["Ocp-Apim-Trace"]
        del api_request_detail_obj.headers["transactionId"]
        expected_data_path = os.path.join(directory, "jsons", "event_notifications_handshake.json")
        api_request_detail_obj.body_data = open_json_file(expected_data_path, "r")

    if status == "options":
        api_request_detail_obj.send_options_request()
    else:
        api_request_detail_obj.send_post_request()


@then(
    parsers.parse(
        "I can see the {status} and {codes} in the response and the response body should match the expected {expected_result}"
    )
)
def validate_response(api_request_detail_obj: ApiRequestDetails, status, codes, expected_result):
    api_request_detail_obj.verify_status_code(int(codes))

    if expected_result != "none":
        if status == "success":
            actual_response_decode = json.loads(api_request_detail_obj.api_response.body())
            assert actual_response_decode["statusCode"] == "202"
        else:
            directory = os.path.dirname(__file__)
            filename = str(expected_result)
            expected_data_path = os.path.join(
                directory,
                "jsons",
                "expected_responses",
                "event_notification",
                filename + ".json",
            )
            api_request_detail_obj.verify_response_from_file(expected_data_path)
