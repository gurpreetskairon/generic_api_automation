import os
from datetime import datetime

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario


@scenario("test participant Idp link API if flt can be updated successfully for given alternateid")
def test_participant_link_positive_flow():
    """participant Idp link API if flt can be updated successfully for given alternate id."""


@scenario("Verify error when send an invalid or blank data")
def test_participant_link_negative_data_flow():
    """Verify error when send an invalid or blank data."""


@scenario("invalid API token should throw error")
def test_participant_link_negative_api_flow():
    """invalid API token should throw error."""


@scenario("Send request with an alternate id which does not exist in CMS throws error")
def test_participant_link_negative_flow_invalid_cms_id():
    """Send request with an alternate id which does not exist in CMS throws error"""


@given(
    parsers.parse(
        "I would like to send a request with different {transaction_id} , {channel_id}, {alternate_id} , "
        "{flt}, {privacy_domain}, {idp}, {ciam_id} and {reference_type_code}"
    )
)
def send_valid_request(
    transaction_id,
    channel_id,
    alternate_id,
    flt,
    privacy_domain,
    idp,
    ciam_id,
    reference_type_code,
    api_request_detail_obj: ApiRequestDetails,
):
    setup_basic_info(api_request_detail_obj, RestDetails.weka_form_data_token_dev, "weka", "post")
    # set none values to be blank
    if alternate_id == "None":
        alternate_id = ""
    if privacy_domain == "None":
        privacy_domain = ""
    if transaction_id == "None":
        transaction_id = ""
    if channel_id == "None":
        channel_id = ""
    if flt == "None":
        flt = ""
    if idp == "None":
        idp = ""
    if ciam_id == "None":
        ciam_id = ""
    if reference_type_code == "None":
        reference_type_code = ""
    if flt == "INVALID_TOKEN":
        api_request_detail_obj.headers = {"Authorization": "bearer 213141"}

    api_request_detail_obj.body_data = {  # Store the request body in context
        "transactionId": transaction_id,
        "requestDateTime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        "channelId": channel_id,
        "alternateId": alternate_id,
        "flt": flt,
        "privacyDomain": privacy_domain,
        "idp": idp,
        "referenceTypeCode": reference_type_code,
        "ciamId": ciam_id,
    }

    api_request_detail_obj.send_post_request()


@then("I should receive a response with status code 200")
def verify_status_code_ok(api_request_detail_obj: ApiRequestDetails):
    api_request_detail_obj.verify_status_code(200)


@then("I should receive a response with status code 409")
def verify_invalid_status_code(api_request_detail_obj: ApiRequestDetails):
    api_request_detail_obj.verify_status_code(409)


@then("I should receive a response with status code 401")
def verify_status_code_failed(api_request_detail_obj: ApiRequestDetails):
    api_request_detail_obj.verify_status_code(401)


@then(parsers.parse("the API response body and status should match the expected {expected_file}"))
def then_the_response_should_match_expected_message(expected_file, api_request_detail_obj: ApiRequestDetails):
    # Construct the expected file path dynamically
    directory = os.path.dirname(__file__)
    filename = str(expected_file)
    expected_data_path = os.path.join(directory, "result_jsons", filename + ".json")
    api_request_detail_obj.verify_response_from_file(expected_data_path)
