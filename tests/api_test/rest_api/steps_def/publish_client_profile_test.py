import json
import os
from datetime import datetime

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from default_config import APIM_SUBSCRIPTION_KEY
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario


@scenario("Check the status of publishing client profile")
def test_check_the_status_of_publishing_client_profile():
    pass


@given(parsers.parse("I send a request with {status}"))
def build_and_send_request(api_request_detail_obj: ApiRequestDetails, status):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "publish_client_endpoint",
    )
    if status == "Key missing":
        api_request_detail_obj.headers = {
            "transactionId": "PublishClientProfile_AutoTest",
            "sourceSystem": "CMS",
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventType": "CREATE",
        }
    elif status == "Header missing":
        api_request_detail_obj.headers = {"apimSubscriptionKey": APIM_SUBSCRIPTION_KEY}
    else:
        api_request_detail_obj.headers = {
            "transactionId": "PublishClientProfile_AutoTest",
            "sourceSystem": "CMS",
            "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
            "sourceEventType": "CREATE",
        }

    if status != "Body missing":
        directory = os.path.dirname(__file__)
        expected_data_path = os.path.join(directory, "jsons", "publish_client.json")
        with open(expected_data_path, "r") as file:
            api_request_detail_obj.body_data = json.load(file)

    api_request_detail_obj.send_post_request()


@then(
    parsers.parse(
        "I can see status {codes} in the response and the response body should match the expected {expected_result}"
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
            "publish_client",
            filename + ".json",
        )
        api_request_detail_obj.verify_response_from_file(expected_data_path)
