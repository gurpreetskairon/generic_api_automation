import allure
import pytest
from pytest_bdd import given, parsers, then

from apps.services.integration_soap.payload_data.dp603 import url_azure, url_iib
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp603_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check the responses are the same across different endpoints
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2937", "User Story")
@scenario("Check whether the DP603 responses are the same across different endpoints")
def test_check_dp603_positive():
    """Check whether the DP603 responses are the same across different endpoints"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check the responses with different conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2937", "User Story")
@scenario("Check DP603 responses are the same across different endpoints with different conditions")
def test_check_dp603_different_conditions():
    """Check DP603 responses are the same across different endpoints with different conditions"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check the responses with different jws
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2937", "User Story")
@scenario("Check DP603 responses are the same across different endpoints with different jws")
@pytest.mark.skip("Test no longer covered/required")
def test_check_dp603_different_jws_conditions():
    """Check DP603 responses are the same across different endpoints with different jws"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    iib_payload = dp603_payload_setup(swn="021238295")
    azure_payload = dp603_payload_setup(swn="021238295", azure=True)
    payloads = {"iib_headers": iib_payload, "azure_headers": azure_payload}
    return payloads


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    iib_payload = dp603_payload_setup(swn="021238295", conditions=conditions)
    azure_payload = dp603_payload_setup(swn="021238295", conditions=conditions, azure=True)
    payloads = {"iib_headers": iib_payload, "azure_headers": azure_payload, "conditions": conditions}

    return payloads


@given("I send inquire participant request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP603", system="IIB", sub_system="STAR")
    return api_client.send_get_request(url_iib(endpoint, payload), headers=payload["iib_headers"], raise_on_error=False)


@given("I send the inquire participant request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP603", system="AZURE")
    return api_client.send_get_request(
        url_azure(endpoint, payload), headers=payload["azure_headers"], raise_on_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP603")
def compare_all_responses(api_client, response_iib, response_azure):
    assert response_iib[1] == response_azure[1], (
        f"Status code mismatch: IIB={response_iib[1]}, Azure={response_azure[1]}"
    )
    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP603")
