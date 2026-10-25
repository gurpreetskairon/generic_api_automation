import os
from datetime import datetime

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario


@scenario("Check inquire provider member with valid responses")
def test_check_inquire_provider_member_with_valid_responses():
    """Check inquire provider member with valid responses."""


@scenario("Check inquire provider member with invalid responses")
def test_check_inquire_provider_member_with_invalid_responses():
    """Check inquire provider member with invalid responses."""


@given(
    parsers.parse(
        "I would like to send a request with different {external_id}, {external_id_type}, "
        "{transaction_id}, {channel_id} and {flt_id}"
    )
)
def send_valid_request(
    external_id,
    external_id_type,
    transaction_id,
    channel_id,
    flt_id,
    api_request_detail_obj: ApiRequestDetails,
):
    setup_basic_info(api_request_detail_obj, RestDetails.weka_form_data_token_dev, "weka", "get")

    # set none values to be blank
    if external_id == "None":
        external_id = ""
    if external_id_type == "None":
        external_id_type = ""
    if transaction_id == "None":
        transaction_id = ""
    if channel_id == "None":
        channel_id = ""
    if flt_id == "None":
        flt_id = ""

    api_request_detail_obj.param_data = {
        "externalID": external_id,
        "externalIDType": external_id_type,
        "transactionID": transaction_id,
        "channelID": channel_id,
        "fltID": flt_id,
        "requestDateTime": datetime.today().strftime("%Y%m%dT%H%M%S"),
    }
    api_request_detail_obj.send_get_request()


@then("I should receive a response with status code 200")
def verify_status_code_ok(api_request_detail_obj: ApiRequestDetails):
    api_request_detail_obj.verify_status_code(200)


@then("I should receive a response with status code 409")
def verify_invalid_status_code(api_request_detail_obj: ApiRequestDetails):
    api_request_detail_obj.verify_status_code(409)


@then(parsers.parse("I can see the response should match the expected values defined in {expected_file}"))
def verify_response_from_file(api_request_detail_obj: ApiRequestDetails, expected_file):
    directory = os.path.dirname(__file__)
    filename = str(expected_file)
    expected_data_path = os.path.join(directory, "result_jsons", filename + ".json")
    api_request_detail_obj.verify_response_from_file(expected_data_path)
