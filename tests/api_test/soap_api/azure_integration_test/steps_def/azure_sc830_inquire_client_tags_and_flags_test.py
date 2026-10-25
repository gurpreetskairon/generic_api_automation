import re
from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.payload_setup import build_api_endpoint, sc830_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


@pytest.mark.skip(reason="need to find new data")
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Check successful transaction response with program tags and client flags
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 successful transaction response with programme tags and client flags")
def test_check_sc830_successful_transaction_response_with_programme_tags_and_client_flags():
    """Check SC830 successful transaction response with programme tags and client flags"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Check program tag category and tag details returned for the client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 programme tag category and tag details returned for the client")
def test_check_sc830_programme_tag_category_and_tag_details_returned_for_the_client():
    """Check SC830 programme tag category and tag details returned for the client"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Check SC830 client flag details returned for the client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 client flag details returned for the client")
def test_check_sc830_client_flag_details_returned_for_the_client():
    """Check SC830 client flag details returned for the client"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Check SC830 response when the client has no current program tags
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 response when the client has no current programme tags")
def test_check_sc830_response_when_the_client_has_no_current_programme_tags():
    """Check SC830 response when the client has no current programme tags"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Check SC830 response when the client has no current flags
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 response when the client has no current flags")
def test_check_sc830_response_when_the_client_has_no_current_flags():
    """Check SC830 response when the client has no current flags"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 6 - Check response when the client has no current program tags and no current flags
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 response when the client has no current programme tags and no current flags")
def test_check_sc830_response_when_the_client_has_no_current_programme_tags_and_no_current_flags():
    """Check SC830 response when the client has no current programme tags and no current flags"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 7 - Check SC830 response when the client does not exist in CMS
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 response when the client does not exist in CMS")
def test_check_sc830_response_when_the_client_does_not_exist_in_cms():
    """Check SC830 response when the client does not exist in CMS"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 8 - Check response when the client number is invalid or missing
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 response when the client number is invalid or missing")
def test_check_sc830_response_when_the_client_number_is_invalid_or_missing():
    """Check SC830 response when the client number is invalid or missing"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 9 - Check SC830 response when the user is not recognised
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2844", "User Story")
@scenario("Check SC830 response when the user is not recognised")
def test_check_sc830_response_when_the_user_is_not_recognised():
    """Check SC830 response when the user is not recognised"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I created the correct api payload", target_fixture="payload")
def create_correct_payload():
    return sc830_payload_setup()


@given(parsers.parse("I created the correct api payload for {client_type}"), target_fixture="payload")
def create_correct_payload_for_client_type(client_type):
    return sc830_payload_setup(client_type)


@given(parsers.parse("I created the api payload for {negative_condition}"), target_fixture="payload")
def create_payload_for_negative_condition(negative_condition):
    return sc830_payload_setup(negative_condition)


@given(
    "I sent the inquire participant request for client tags and flags to the Azure endpoint", target_fixture="response"
)
def send_inquire_participant_request_for_client_tags_and_flags(api_client, payload):
    sc830_endpoint = build_api_endpoint("SC830", system="AZURE")

    return api_client.send_post_request(sc830_endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the Transaction Successful returned")
def verify_status_message(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, "Transaction Successful")


@then(parsers.parse("I can see result code {result_code} returned"))
def verify_result_code(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I can see result message "{result_message}" returned'))
def verify_result_message(api_client, response, result_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, result_message)


@then("I can see the request auditId, requestDateTime and transactionId returned in SOAP response header")
def verify_request_header_details_returned(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.audit_id, payload["audit_id"])

    api_client.check_value_in_xml_response(response, dot_xml_pattern.request_datetime, payload["request_date_time"])

    api_client.check_value_in_xml_response(response, dot_xml_pattern.transaction_id, payload["transaction_id"])


@then("I can see the clientNumber returned in the response SOAP header serviceResult")
def verify_client_number_returned(api_client, response, payload):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_number, payload["client_id"])


@then("I can see programme tag details returned")
def verify_programme_tag_details_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.programme_tag_category_code, "CSMGMTAPPR")

    api_client.check_value_in_xml_response(
        response,
        dot_xml_pattern.programme_tag_category_description,
        "Indicates the formal approach to case managing the client."
    )

    api_client.check_value_in_xml_response(response, dot_xml_pattern.programme_tag_code, "ISRP")

    api_client.check_value_in_xml_response(
        response, dot_xml_pattern.programme_tag_description, "Integrated Service Response"
    )


@then("I can see client flag details returned")
def verify_client_flag_details_returned(api_client, response):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_flag_code, "ENBCLKENL")

    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_flag_description, "Enable Click To Enrol")


@then(parsers.parse('I can see programme tag category code "{category_code}" returned'))
def verify_programme_tag_category_code_returned(api_client, response, category_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.programme_tag_category_code, category_code)


@then(parsers.parse('I can see programme tag category description "{category_description}" returned'))
def verify_programme_tag_category_description_returned(api_client, response, category_description):
    api_client.check_value_in_xml_response(
        response, dot_xml_pattern.programme_tag_category_description, category_description
    )


@then(parsers.parse('I can see programme tag code "{tag_code}" returned'))
def verify_programme_tag_code_returned(api_client, response, tag_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.programme_tag_code, tag_code)


@then(parsers.parse('I can see programme tag description "{tag_description}" returned'))
def verify_programme_tag_description_returned(api_client, response, tag_description):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.programme_tag_description, tag_description)


@then(parsers.parse('I can see client flag code "{flag_code}" returned'))
def verify_client_flag_code_returned(api_client, response, flag_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_flag_code, flag_code)


@then(parsers.parse('I can see client flag description "{flag_description}" returned'))
def verify_client_flag_description_returned(api_client, response, flag_description):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.client_flag_description, flag_description)


@then(parsers.re(r"I can see subresult code (?P<subresult_code>\d+) returned"))
def verify_subresult_code_returned(api_client, response, subresult_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.subresult_code, subresult_code)


@then(parsers.parse('I can see subresult message "{subresult_message}" returned'))
def verify_subresult_message_returned(api_client, response, subresult_message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.subresult_message, subresult_message)


@then(parsers.re(r'I can see subresult code (?P<subresult_code>\d+) and message "(?P<subresult_message>.+)" returned'))
def verify_subresult_code_and_message_returned(response, subresult_code, subresult_message):
    response_text = str(response)

    pattern = (
        rf"<[^:>]*:?subResult>"
        rf".*?<[^:>]*:?message>{re.escape(subresult_message)}</[^:>]*:?message>"
        rf".*?<[^:>]*:?result>{subresult_code}</[^:>]*:?result>"
        rf".*?</[^:>]*:?subResult>"
    )

    assert re.search(pattern, response_text, re.DOTALL), (
        f"Subresult code {subresult_code} with message '{subresult_message}' " f"was not found in the response"
    )
