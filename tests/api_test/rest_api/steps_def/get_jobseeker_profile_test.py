import os
from datetime import datetime

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from default_config import JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario


@scenario("Check the status of getting jobseeker profile")
def test_check_the_status_of_getting_jobseeker_profile():
    pass


@given(parsers.parse("I send a request with {status}"))
def build_and_send_request(api_request_detail_obj: ApiRequestDetails, status):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "jobseeker_profile_endpoint",
    )
    if status == "Completed":
        api_request_detail_obj.param_data = {"clientNumber": "c1"}
    elif status == "Incomplete":
        api_request_detail_obj.param_data = {"clientNumber": "c2"}
    elif status == "Invalid":
        api_request_detail_obj.param_data = {"clientNumber": ""}
    elif status == "Internal Server Error":
        api_request_detail_obj.param_data = {"clientNumber": "c5"}

    api_request_detail_obj.headers = {
        "apimSubscriptionKey": JS_PROFILE_STATUS_APIM_SUBSCRIPTION_KEY,
        "transactionId": f"JobSeekerStatus{status}_AutoTest",
        "sourceSystem": "AISNP",
        "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        "Ocp-Apim-Trace": "true",
    }
    api_request_detail_obj.send_get_request()


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
            "jobseekers_profile_status",
            filename + ".json",
        )
        api_request_detail_obj.verify_response_from_file(expected_data_path)
