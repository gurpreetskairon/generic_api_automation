import allure
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc157_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC157 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3421", "API-3421")
@scenario("Compare SC157 successful response")
def test_compare_sc157_successful_response():
    """Compare SC157 successful response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC157 responses with invalid data
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3421", "API-3421")
@scenario("Compare SC157 responses with invalid data")
def test_compare_sc157_response_with_invalid_data():
    """Compare SC157 responses with invalid data"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    iib_params, iib_headers = sc157_payload_setup()
    azure_params, azure_headers = sc157_payload_setup(azure=True)
    payloads = {
        "iib_headers": iib_headers,
        "iib_params": iib_params,
        "azure_headers": azure_headers,
        "azure_params": azure_params,
    }
    return payloads


@given(parsers.parse("I create the correct api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    iib_params, iib_headers = sc157_payload_setup(conditions=conditions)
    azure_params, azure_headers = sc157_payload_setup(conditions=conditions, azure=True)
    payloads = {
        "iib_headers": iib_headers,
        "iib_params": iib_params,
        "azure_headers": azure_headers,
        "azure_params": azure_params,
    }
    return payloads


@given("I send the request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC157", system="IIB")
    return api_client.send_get_request(
        endpoint, headers=payload["iib_headers"], params=payload["iib_params"], raise_on_error=False
    )


@given("I send the request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC157", system="AZURE")
    return api_client.send_get_request(
        endpoint, headers=payload["azure_headers"], params=payload["azure_params"], raise_on_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib[0], response_azure[0], "SC157")
