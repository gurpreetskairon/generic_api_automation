import os
from datetime import datetime

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from default_config import PUBLISH_OBLIGATIONS_APIM_SUBSCRIPTION_KEY
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario
from utils.common_utils.helper_functions.json_parser import open_json_file


@scenario("AIS publish obligation")
def test_publish_obligations():
    pass


@scenario("AIS sync obligation")
def test_sync_obligations():
    pass


@scenario("Obman sync direct")
def test_obman_sync_obligations():
    pass


@given(parsers.parse("I send an api request with {body} body to publish a clients obligations"))
def build_and_send_publish_obligations_post_request(api_request_detail_obj: ApiRequestDetails, body):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "publish_obligations_endpoint",
    )
    api_request_detail_obj.headers = {
        "correlationId": f"Obligations_{body}_AutoTest_{datetime.today().strftime('%H:%M_%d-%m-%y')}",
        "apimSubscriptionKey": PUBLISH_OBLIGATIONS_APIM_SUBSCRIPTION_KEY,
        "transactionId": f"Obligations_{body}_AutoTest",
        "sourceSystem": "SWIFTT",
        "sourceEventType": "CREATE",
        "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
    }

    directory = f"{os.path.dirname(__file__)}\\jsons\\publish_sync_obligations"
    if body == "null_values":
        expected_data_path = os.path.join(directory, "publish_obligations_null_values.json")
    else:
        expected_data_path = os.path.join(directory, "publish_obligations.json")

    api_request_detail_obj.body_data = open_json_file(expected_data_path, "r")
    api_request_detail_obj.send_post_request()


@given(parsers.parse("I send an api request with {body} body to sync a clients obligations"))
def build_and_send_sync_obligations_post_request(api_request_detail_obj: ApiRequestDetails, body):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "sync_obligations_endpoint",
    )
    api_request_detail_obj.headers = {
        "correlationId": f"Obligations_{body}_AutoTest_{datetime.today().strftime('%H:%M_%d-%m-%y')}",
        "apimSubscriptionKey": PUBLISH_OBLIGATIONS_APIM_SUBSCRIPTION_KEY,
        "transactionId": f"Obligations_{body}_AutoTest",
        "sourceSystem": "SWIFTT",
        "sourceEventType": "CREATE",
        "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
    }

    directory = f"{os.path.dirname(__file__)}\\jsons\\publish_sync_obligations"
    if body == "null_values":
        expected_data_path = os.path.join(directory, "sync_obligations_null_values.json")
    else:
        expected_data_path = os.path.join(directory, "sync_obligations.json")

    api_request_detail_obj.body_data = open_json_file(expected_data_path, "r")
    api_request_detail_obj.send_post_request()


@given(parsers.parse("I send an api request to obman"))
def build_and_send_obman_sync_obligations_post_request(
    api_request_detail_obj: ApiRequestDetails,
):
    setup_basic_info(api_request_detail_obj, RestDetails.integration_data_token, "obman_endpoint")
    api_request_detail_obj.headers = {
        "correlationId": f"Obligations_obman_AutoTest_{datetime.today().strftime('%H:%M_%d-%m-%y')}",
        "apimSubscriptionKey": PUBLISH_OBLIGATIONS_APIM_SUBSCRIPTION_KEY,
        "transactionId": "Obligations_obman_AutoTest",
        "sourceSystem": "SWIFTT",
        "sourceEventType": "CREATE",
        "sourceEventDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
    }

    directory = f"{os.path.dirname(__file__)}\\jsons\\publish_sync_obligations"
    expected_data_path = os.path.join(directory, "sync_obligations.json")
    api_request_detail_obj.body_data = open_json_file(expected_data_path, "r")
    api_request_detail_obj.send_post_request()


@then(
    parsers.parse(
        "I can see status {codes} in the response and the response body should match the expected {expected_result}"
    )
)
def validate_response(api_request_detail_obj: ApiRequestDetails, codes, expected_result):
    api_request_detail_obj.verify_status_code(int(codes))

    if expected_result == "Payload processed successfully":
        assert expected_result in str(api_request_detail_obj.api_response.body())
    else:
        directory = os.path.dirname(__file__)
        filename = str(expected_result)
        expected_data_path = os.path.join(
            directory, "jsons\\expected_responses\\publish_sync_obligations", f"{filename}.json"
        )
        api_request_detail_obj.verify_response_from_file(expected_data_path)
