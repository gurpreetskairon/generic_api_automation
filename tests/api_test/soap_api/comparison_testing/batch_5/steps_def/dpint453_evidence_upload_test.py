from types import SimpleNamespace
import allure
from pytest_bdd import given, parsers, then
from apps.services.integration_soap.payload_data.dpint453.dpint453 import (
    upload_document_id_to_db,
    delete_document_id_from_db
)
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dpint453_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario


dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare dpint453 successful response for uploading documents
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3913", "User Story")
@scenario("Compare dpint453 successful response for uploading documents")
def test_compare_dpint453_successful_response_for_uploading_documents():
    """Compare dpint453 successful response for uploading documents"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare dpint453 successful response for deleting documents
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3913", "User Story")
@scenario("Compare dpint453 successful response for deleting documents")
def test_compare_dpint453_successful_response_for_deleting_documents():
    """Compare dpint453 successful response for deleting documents"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse("I create the api payload with different {conditions} for {method} method"), target_fixture="payload"
)
def create_different_payload(conditions, method):
    iib_request = dpint453_payload_setup(condition=conditions, method=method)
    azure_request = dpint453_payload_setup(condition=conditions, method=method, previous_doc_id=iib_request[3]["documentId"])
    return iib_request, azure_request


@given(parsers.parse("I send a {method} request to the IIB endpoint"), target_fixture="response_iib")
def send_iib_request(api_client, payload, method):
    endpoint = build_api_endpoint("INT453", system="IIB", sub_system="MYMSD")
    if method == "POST":
        response = api_client.send_post_request(endpoint, headers=payload[0][0], payload=payload[0][1], file=payload[0][2])
        upload_document_id_to_db(response)
    elif method == "DELETE":
        response = api_client.send_delete_request(endpoint, headers=payload[0][0], params=payload[0][3])
        delete_document_id_from_db(payload[0][3]["documentId"])
    else:
        raise Exception("Method must be POST or DELETE")

    return response


@given(parsers.parse("I send a {method} request to Azure endpoint"), target_fixture="response_azure")
def send_azure_request(api_client, payload, method):
    endpoint = build_api_endpoint("INT453", system="AZURE")
    if method == "POST":
        response = api_client.send_post_request(endpoint, headers=payload[1][0], payload=payload[1][1], file=payload[1][2],
                                                raise_error=False)
        upload_document_id_to_db(response)
    elif method == "DELETE":
        response = api_client.send_delete_request(endpoint, headers=payload[1][0], params=payload[1][3], raise_on_error=False)
        delete_document_id_from_db(payload[1][3]["documentId"])
    else:
        raise Exception("Method must be POST or DELETE")
    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "DPINT453", exclude_fields=["documentId"])
