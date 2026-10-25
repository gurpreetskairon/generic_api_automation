import allure
from pytest_bdd import given, parsers, then

from apps.services.integration_soap.payload_data.dp604 import url_azure, url_iib
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp604_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check whether the DP604 responses are the same across different endpoints
# ══════════════════════════════════════════════════════════════════════════════════════
@scenario("Check whether the DP604 responses are the same across different endpoints")
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2939", "User Story")
def test_check_dp604_positive():
    """Check whether the DP604 responses are the same across different endpoints"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check the response across different endpoints with different conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2939", "User Story")
@scenario("Check DP604 responses are the same across different endpoints with different conditions")
def test_check_dp604_different_conditions():
    """Check DP604 responses are the same across different endpoints with different conditions"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check the response across different endpoints with different jws
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2939", "User Story")
@scenario("Check DP604 responses are the same across different endpoints with different jws")
def test_check_dp604_different_jws():
    """Check DP604 responses are the same across different endpoints with different jws"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct api payload", target_fixture="payload")
def create_correct_payload():
    iib_payload, iib_params = dp604_payload_setup(swn="021238295")
    azure_payload, azure_params = dp604_payload_setup(swn="021238295", azure=True)
    # iib_params = {"usage": "RESIDENTIAL"}
    azure_params = {}

    payloads = {
        "iib_headers": iib_payload,
        "iib_params": iib_params,
        "azure_headers": azure_payload,
        "azure_params": azure_params,
    }

    return payloads


@given(parsers.parse("I create the api payload with different {conditions}"), target_fixture="payload")
def create_different_payload(conditions):
    iib_payload, iib_params = dp604_payload_setup(swn="021238295", conditions=conditions)
    azure_payload, azure_params = dp604_payload_setup(swn="021238295", conditions=conditions, azure=True)
    if conditions != "missing usage":
        pass
    payloads = {
        "iib_headers": iib_payload,
        "iib_params": iib_params,
        "azure_headers": azure_payload,
        "azure_params": azure_params,
        "conditions": conditions,
    }

    return payloads


@given("I send inquire participant request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("DP604", system="IIB", sub_system="STAR")
    return api_client.send_get_request(
        url_iib(endpoint, payload), headers=payload["iib_headers"], params=payload["iib_params"], raise_on_error=False
    )


@given("I send the inquire participant request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP604", system="AZURE")
    return api_client.send_get_request(
        url_azure(endpoint, payload),
        headers=payload["azure_headers"],
        params=payload["azure_params"],
        raise_on_error=False
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP604")
def compare_all_responses(api_client, response_iib, response_azure):
    assert response_iib[1] == response_azure[1], (
        f"Status code mismatch: IIB={response_iib[1]}, Azure={response_azure[1]}"
    )

    api_client.compare_json_responses(response_iib[0], response_azure[0], "DP604")
