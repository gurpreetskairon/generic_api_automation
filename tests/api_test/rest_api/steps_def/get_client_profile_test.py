from datetime import datetime, timedelta, timezone

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from default_config import APIM_SUBSCRIPTION_KEY, FLTTOKEN, PRIVACY_DOMAIN
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario


@scenario("Check the status of getting client profile")
def test_check_the_status_of_getting_client_profile():
    """Check the status of getting client profile"""


@given(parsers.parse("I send a request with different {header}"))
def build_and_send_request(header, api_request_detail_obj: ApiRequestDetails):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "get_client_profile_endpoint",
    )
    request_date_time = datetime.now(timezone(timedelta(hours=13))).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    authorization = api_request_detail_obj.headers.get("Authorization")
    if header == "Get client":
        api_request_detail_obj.endpoint += "/623141823"
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
            "transactionid": "200-InquireClient",
            "requestDateTime": f"{request_date_time}",
            "sourceSystem": "SEP",
            "Authorization": f"{authorization}",
        }
    elif header == "Get client flt":
        api_request_detail_obj.endpoint += "/623141823"
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
            "transactionid": "200-InquireClients",
            "requestDateTime": f"{request_date_time}",
            "sourceSystem": "CIAM",
            "fltToken": FLTTOKEN,
            "privacyDomain": PRIVACY_DOMAIN,
            "Authorization": f"{authorization}",
        }
    elif header == "Token expired":
        api_request_detail_obj.headers = {
            "transactionid": "51fd3de3-9e36-40e6-91af-b2d3a18b5313",
            "requestDateTime": f"{request_date_time}",
            "sourceSystem": "SEP",
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
        }
    elif header == "Key missing":
        api_request_detail_obj.headers = {
            "transactionid": "51fd3de3-9e36-40e6-91af-b2d3a18b5313",
            "requestDateTime": f"{request_date_time}",
            "sourceSystem": "SEP",
        }
    else:
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
            "transactionid": "200-InquireClient",
            "requestDateTime": f"{request_date_time}",
            "Authorization": f"{authorization}",
        }
    api_request_detail_obj.send_get_request()


@then(parsers.parse("I am receiving different status {codes} and service {results}"))
def validate_response(api_request_detail_obj: ApiRequestDetails, codes, results):
    api_request_detail_obj.verify_status_code(int(codes))
    if codes == "200" and results == "Has Client Information":
        api_request_detail_obj.verify_client_information_from_response()
    else:
        api_request_detail_obj.verify_response_values_from_parms("serviceResults", results)
