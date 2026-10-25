import os
import re
from types import SimpleNamespace

import allure
import pytest
from lxml import etree
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.payload_setup import (
    build_api_endpoint,
    mark_sc827_partner_client_number_used,
    sc827_payload_setup
)
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


@pytest.mark.skip(reason="need to find new data")
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Verify SC827 returns successful response when registering a client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3392", "User Story")
@scenario("Verify SC827 returns successful response when registering a client")
def test_verify_sc827_returns_successful_response_when_registering_a_client():
    """Verify SC827 returns successful response when registering a client."""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Verify SC827 returns unsuccessful response for invalid register client request
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3392", "User Story")
@scenario("Verify SC827 returns unsuccessful response for invalid register client request")
def test_verify_sc827_returns_unsuccessful_response_for_invalid_register_client_request():
    """Verify SC827 returns unsuccessful response for invalid register client request."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the correct SC827 payload for "{condition}"'), target_fixture="payload")
def create_correct_sc827_payload(condition):
    """
    Creates SC827 payload for positive register client scenarios.

    Covered by Scenario 1:
      - valid_register_client_without_partner
      - valid_register_client_with_partner
    """

    return sc827_payload_setup(condition)


@given(parsers.parse('I create the SC827 payload for "{condition}"'), target_fixture="payload")
def create_sc827_payload_for_condition(condition):
    """
    Creates SC827 payload for negative register client scenarios.

    Covered by Scenario 2:
      - missing_mandatory_person_data
      - invalid_ird_number_format
      - ird_number_found_in_another_customer
      - dob_after_system_date
      - partner_client_number_does_not_exist
      - secured_partner_client
      - partner_already_has_current_relationship
      - invalid_marital_status
      - invalid_marital_status_effective_date
      - invalid_person_name_format
      - invalid_person_gender_format
      - invalid_country_of_birth
      - invalid_ethnicity_group
      - invalid_contact_address
      - missing_security_token_id_for_partner
      - existing_client_match_found
      - incorrect_partner_client_number_details
      - partner_address_contact_mismatch
      - invalid_residency_code
      - invalid_residency_class_visa_status_date
      - result_not_recognised
    """

    return sc827_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC827 request to Azure", target_fixture="response")
def send_sc827_request_to_azure(api_client, payload):
    """
    Sends the generated SC827 payload to the Azure endpoint.

    The request body and headers are attached to Allure for debugging and
    manual Azure-vs-IIB comparison if needed.
    """

    azure_pipeline_env = os.getenv("ENVIRONMENT_NAME", "")
    sc827_endpoint = build_api_endpoint("SC827", system="AZURE")

    if azure_pipeline_env.casefold() == "sit":
        sc827_endpoint = str(sc827_endpoint).replace("dev", "sit")

    allure.attach(payload["request_body"], name="SC827 request body", attachment_type=allure.attachment_type.XML)

    allure.attach(str(payload["header"]), name="SC827 request headers", attachment_type=allure.attachment_type.TEXT)

    return api_client.send_post_request(sc827_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then(parsers.parse('the SC827 response should contain result code "{result_code}"'))
def verify_sc827_result_code(api_client, response, result_code):
    """
    Verifies SC827 serviceResult/result.

    Used by:
      - Scenario 1 positive outline
      - Scenario 2 negative outline
    """

    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('the SC827 response should contain result message "{message}"'))
def verify_sc827_result_message(api_client, response, message):
    """
    Verifies SC827 serviceResult/message.

    Used by:
      - Scenario 1 positive outline
      - Scenario 2 negative outline
    """

    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_message, message)


@then("the SC827 response should contain a generated client number")
def verify_sc827_response_contains_generated_client_number(response, payload):
    """
    Verifies generated clientNumber for successful SC827 response.

    Used by Scenario 1 only.

    For the positive partner scenario, the selected partner pool row is marked
    as USED after the new client number is returned.
    """

    client_number = _get_client_number_from_sc827_response(response)

    assert client_number is not None, "clientNumber is missing in SC827 response"
    assert str(client_number).strip() != "", "clientNumber is empty in SC827 response"
    assert re.match(
        r"^\d+$", str(client_number).strip()
    ), f"clientNumber should be numeric, but actual value was: {client_number}"

    if payload.get("condition") == "valid_register_client_with_partner":
        mark_sc827_partner_client_number_used(
            pool_id=payload.get("partner_pool_id"), created_client_number=str(client_number).strip()
        )


@then(parsers.parse('the SC827 response should contain sub-result code "{subresult_code}"'))
def verify_sc827_subresult_code(api_client, response, subresult_code):
    """
    Verifies SC827 serviceResult/subResult/result.

    Used by Scenario 2 negative outline.
    """

    api_client.check_value_in_xml_response(response, dot_xml_pattern.subresult_code, subresult_code)


@then(parsers.parse('the SC827 response should contain sub-result message "{subresult_message}"'))
def verify_sc827_subresult_message(response, subresult_message):
    """
    Verifies SC827 serviceResult/subResult/message.

    Used by Scenario 2 negative outline.

    Some SC827 sub-result messages contain dynamic CMS values.
    Example:
      existing_client_match_found returns:
      Create client failed. Matches have been found for customer numbers: 5262...

    Therefore this step validates that the expected static message text
    is present in the actual response body.
    """

    response_body = _get_response_body(response)

    assert response_body is not None, "Response body is None."

    response_text = response_body.decode("utf-8") if isinstance(response_body, bytes) else str(response_body)

    assert subresult_message in response_text, (
        f"Expected sub-result message was not found in SC827 response.\n"
        f"Expected: {subresult_message}\n"
        f"Actual response: {response_text}"
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Helper functions
# ══════════════════════════════════════════════════════════════════════════════════════
def _get_response_body(response):
    """
    Extracts XML body from SOAP validator response.

    Current framework usually returns:
      (response_body, status_code)
    """

    if isinstance(response, tuple):
        return response[0]

    if isinstance(response, list):
        return response[0]

    return response


def _get_client_number_from_sc827_response(response):
    """
    Extracts generated clientNumber from SC827 response.

    Uses local-name() because SC827 response may use namespace prefixes, for example:
      <hdr:clientNumber>
    """

    response_body = _get_response_body(response)

    if response_body is None:
        return None

    if isinstance(response_body, bytes):
        xml_root = etree.fromstring(response_body)
    else:
        xml_root = etree.fromstring(str(response_body).encode("utf-8"))

    result = xml_root.xpath("//*[local-name()='clientNumber']/text()")

    if not result:
        return None

    return result[0]
