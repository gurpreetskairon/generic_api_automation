import json

import allure
import pytest
from pytest_bdd import given, parsers, then

import apps.services.integration_soap.expected_responses.dp603_responses_azure as responses
from apps.services.integration_soap.payload_data.dp603 import url_azure
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp603_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check whether the DP603 azure responses match whats on file
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2935", "User Story")
@scenario("Check whether the DP603 azure responses match whats on file")
def test_check_dp603_azure_positive():
    """Check whether the DP603 azure responses match what's on file"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check whether the azure responses match whats on file with varying conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2935", "User Story")
@scenario("Check whether the DP603 azure responses match whats on file with varying conditions")
def test_check_dp603_azure_different_conditions():
    """Check whether the DP603 azure responses match what's on file with varying conditions"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check whether the azure responses match whats on file with varying jws conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2935", "User Story")
@scenario("Check whether the DP603 azure responses match whats on file with varying jws conditions")
def test_check_dp603_different_jws_conditions():
    """Check whether the DP603 azure responses match whats on file with varying jws conditions"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct payload", target_fixture="payload")
def create_correct_payload():
    return {"headers": dp603_payload_setup(swn="021238295", azure=True)}


@given(parsers.parse("I create the payload with {conditions}"), target_fixture="payload")
def create_different_azure_payload(conditions):
    if conditions == "invalid clientID":
        payload = {
            "headers": dp603_payload_setup(swn="000000000", conditions=conditions, azure=True),
            "conditions": conditions,
        }
    else:
        payload = {
            "headers": dp603_payload_setup(swn="021238295", conditions=conditions, azure=True),
            "conditions": conditions,
        }
    return payload


@given("I send the request to the Azure DP603 endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("DP603", system="AZURE")
    response = api_client.send_get_request(
        url_azure(endpoint, payload), headers=payload["headers"], raise_on_error=False
    )
    print(f"Condition: {payload.get('conditions', 'positive_scenario')}")
    print("Azure response:", response)

    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("I see the response matches the {conditions} expected response and {status} on file"))
def validate_response(api_client, response_azure, conditions, status):
    api_client.compare_status_code(status, str(response_azure[1]))
    assert str(response_azure[1]) == status
    error_400_conditions = [
        "missing transactionId",
        "missing requestDateTime",
        "invalid jws method",
        "invalid requestDateTime",
        "unencoded clientID",
        "missing jws",
        "invalid jws key",
        "invalid jws algorithm",
        "invalid query string",
        "missing sourceSystem",
        "missing securityTokenId",
    ]
    # error_500_conditions = ["missing securityTokenId"]

    if conditions in error_400_conditions:
        assert response_azure[0] == ""
        return
    elif conditions == "invalid securityTokenId":
        expected_response = json.dumps(responses.invalid_security_token_id).replace('"null"', "null")
        api_client.compare_json_responses(expected_response, response_azure[0], "DP603")
    # elif conditions in error_500_conditions:
    #     expected_response = json.dumps(responses.error_500).strip('"')
    #     api_client.compare_error_strings(expected_response, response_azure[0], "DP603", system="on file")
    elif conditions == "invalid clientID":
        expected_response = json.dumps(responses.invalid_client_id).replace('"null"', "null")
        api_client.compare_json_responses(expected_response, response_azure[0], "DP603")
    else:
        expected_response = json.dumps(responses.positive_scenario)
        api_client.compare_json_responses(expected_response, response_azure[0], "DP603")
