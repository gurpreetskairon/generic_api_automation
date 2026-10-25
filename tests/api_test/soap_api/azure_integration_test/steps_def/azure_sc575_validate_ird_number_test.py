import os
from types import SimpleNamespace
from typing import cast

import allure
import pytest
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc575_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


@pytest.mark.skip(reason="need to find new data")
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify successful match response when all supplied client details are correct
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Verify successful match response when all supplied client details are correct")
def test_sc575_successful_match_response():
    """Verify SC575 successful match response when all supplied client details are correct"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify no match response when supplied client details do not match
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Verify no match response when supplied client details do not match")
def test_sc575_no_match_response():
    """Verify SC575 no match response when supplied client details do not match"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Verify validation response when mandatory request parameters are missing or invalid
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Verify validation response when mandatory request parameters are missing or invalid")
def test_sc575_mandatory_request_parameters_missing_or_invalid():
    """Verify SC575 validation response when mandatory request parameters are missing or invalid"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Verify validation response when IRD is 9 digits but not valid for the customer type
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Verify validation response when IRD is 9 digits but not valid for the customer type")
def test_sc575_ird_not_valid_for_customer_type():
    """Verify SC575 validation response when IRD is 9 digits but not valid for the customer type"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Verify validation response when transactionId is missing or invalid
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Verify validation response when transactionId is missing or invalid")
def test_sc575_transaction_id_missing_or_invalid():
    """Verify SC575 validation response when transactionId is missing or invalid"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I have access to the SC575 Azure endpoint")
def verify_sc575_azure_endpoint_available():
    sc575_endpoint = build_api_endpoint("SC575", system="AZURE")

    if not sc575_endpoint:
        raise ValueError("SC575_AZURE_URL environment variable is not set")


@given("I have a valid SC575 SOAP request payload", target_fixture="payload")
def create_valid_sc575_soap_request_payload():
    return sc575_payload_setup(conditions="match")


@given("I create an SC575 payload with valid IRD, name, date of birth and address", target_fixture="payload")
def create_sc575_match_payload():
    return sc575_payload_setup(conditions="match")


@given("I create an SC575 payload with a valid IRD", target_fixture="payload")
def create_sc575_valid_ird_payload():
    return sc575_payload_setup(conditions="match")


@given(parsers.parse('I update the payload with a non-matching "{field}"'), target_fixture="payload")
def update_payload_with_non_matching_field(field):
    if field == "name":
        return sc575_payload_setup(conditions="no_match_name")

    if field == "dateOfBirth":
        return sc575_payload_setup(conditions="no_match_dateOfBirth")

    raise ValueError(f"Unsupported SC575 non-matching field: {field}")


@given(
    parsers.parse('I create an SC575 payload with invalid or missing "{field}" using "{condition}"'),
    target_fixture="payload"
)
def create_sc575_invalid_or_missing_payload(field, condition):
    return sc575_payload_setup(field=field, conditions=condition)


@given(
    "I create an SC575 payload with a 9 digit IRD number that is not valid or does not match the customer type",
    target_fixture="payload"
)
def create_sc575_invalid_customer_type_ird_payload():
    return sc575_payload_setup(conditions="invalid_customer_type_ird")


@given(parsers.parse('I create an SC575 payload with "{transaction_id_condition}"'), target_fixture="payload")
def create_sc575_transaction_id_payload(transaction_id_condition):
    return sc575_payload_setup(conditions=transaction_id_condition)


@given("I create an SC575 payload with a valid IRD number", target_fixture="payload")
def create_sc575_valid_ird_number_payload():
    return sc575_payload_setup(conditions="match")


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the request to the Azure endpoint", target_fixture="response")
def send_sc575_request_to_azure_endpoint(api_client, payload):
    sc575_endpoint = build_api_endpoint("SC575", system="AZURE")

    return api_client.send_post_request(sc575_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse("the HTTP status code should be {status_code:d}"))
def verify_http_status_code(response, status_code):
    actual_status_code = response[1]

    assert actual_status_code == status_code, (
        f"Expected HTTP status code {status_code}, " f"but got {actual_status_code}. Response: {response[0]}"
    )


@then(parsers.parse('the SOAP response result code should be "{result_code}"'))
def verify_soap_response_result_code(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('the SOAP response message should be "{result_message}"'))
def verify_soap_response_message(api_client, response, result_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, result_message)


@then(parsers.parse('the match outcome should be "{match_outcome}"'))
def verify_match_outcome(api_client, response, match_outcome):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.match_outcome, match_outcome)


def get_sc575_azure_endpoint():
    azure_pipeline_env = os.getenv("ENVIRONMENT_NAME")
    sc575_endpoint = os.getenv("SC575_AZURE_URL")

    if not sc575_endpoint:
        raise ValueError("SC575_AZURE_URL environment variable is not set")

    if azure_pipeline_env and azure_pipeline_env.casefold() == "sit":
        sc575_endpoint = sc575_endpoint.replace("dev", "sit")

    return sc575_endpoint
