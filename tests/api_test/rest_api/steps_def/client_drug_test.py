from datetime import datetime, timedelta, timezone

from pytest_bdd import given, parsers, then

from apps.services.integration_api.api_content import ApiRequestDetails
from default_config import APIM_SUBSCRIPTION_KEY
from utils.api_utils.helper.api_endpoint_builders import setup_basic_info
from utils.api_utils.helper.rest_details import RestDetails
from utils.bdd_utils.scenario import scenario


@scenario("Check the status of client drug test")
def test_check_the_status_of_client_drug_test():
    """Check the status of client drug test"""


@given(parsers.parse("I send a request with different {header}"))
def send_request_with_status(header, api_request_detail_obj: ApiRequestDetails):
    setup_basic_info(
        api_request_detail_obj,
        RestDetails.integration_data_token,
        "client_drug_endpoint",
    )
    request_date_time = datetime.now(timezone(timedelta(hours=13))).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    authorization = api_request_detail_obj.headers.get("Authorization")
    if header == "Check drug test referral":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
            "transactionid": "200-checkDrugTestReferral",
            "requestDateTime": f"{request_date_time}",
            "sourceSystem": "SEP",
            "Authorization": f"{authorization}",
        }
    elif header == "Token missing":
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
            "transactionid": "51fd3de3-9e36-40e6-91af-b2d3a18b5313",
            "requestDateTime": f"{request_date_time}",
            "sourceSystem": "SEP",
        }
    elif header == "Key missing":
        api_request_detail_obj.headers = {
            "transactionid": "51fd3de3-9e36-40e6-91af-b2d3a18b5313",
            "requestDateTime": f"{request_date_time}",
            "sourceSystem": "SEP",
            "Authorization": f"{authorization}",
        }
    else:
        api_request_detail_obj.headers = {
            "apimSubscriptionKey": APIM_SUBSCRIPTION_KEY,
            "transactionid": "51fd3de3-9e36-40e6-91af-b2d3a18b5313",
            "requestDateTime": f"{request_date_time}",
            "Authorization": f"{authorization}",
        }
    api_request_detail_obj.send_get_request()


@then(parsers.parse("I am receiving different status {codes} and service {results}"))
def validate_response(api_request_detail_obj: ApiRequestDetails, codes, results):
    api_request_detail_obj.verify_status_code(int(codes))
    if results == "Transaction Successful":
        results = [results, "Transaction Successful - Notification not found"]
    api_request_detail_obj.verify_response_values_from_parms("serviceResults", results)
