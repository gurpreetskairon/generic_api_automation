from pytest_bdd import given, parsers, then, when

from apps.services.integration_soap.payload_data.dp898 import compare_dp898_responses, url_azure, url_datapower
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp898_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check whether the DP898 responses are the same across different endpoints
# ══════════════════════════════════════════════════════════════════════════════════════
@scenario("Check whether the DP898 responses are the same across different endpoints")
def test_check_dp898_positive():
    """Check whether the DP898 responses are the same across different endpoints."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check responses across different endpoints with different conditions
# ══════════════════════════════════════════════════════════════════════════════════════
@scenario("Check DP898 responses are the same across different endpoints with different conditions")
def test_check_dp898_different_conditions():
    """Check DP898 responses across endpoints for different conditions."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create the correct DP898 api payload", target_fixture="payload")
def create_correct_dp898_payload(formatted_datetime):
    return dp898_payload_setup(condition="valid_client", date_time=formatted_datetime)


@given(parsers.parse('I create the DP898 api payload with different "{condition}"'), target_fixture="payload")
def create_dp898_payload_with_different_conditions(condition, formatted_datetime):
    return dp898_payload_setup(condition=condition, date_time=formatted_datetime)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the DP898 request to the DataPower endpoint", target_fixture="response_datapower")
def send_dp898_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint("DP898", system="IIB", sub_system="MYMSD")
    request_url = url_datapower(endpoint, payload)

    return api_client.send_get_request(request_url, headers=payload["datapower_headers"], raise_on_error=False)


@when("I send the same DP898 request to the Azure endpoint", target_fixture="response_azure")
def send_dp898_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP898", system="AZURE", sub_system="NONE")
    request_url = url_azure(endpoint, payload)

    return api_client.send_get_request(request_url, headers=payload["azure_headers"], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the DP898 responses are identical")
def validate_dp898_responses(api_client, response_datapower, response_azure):
    compare_dp898_responses(api_client, response_datapower, response_azure)
