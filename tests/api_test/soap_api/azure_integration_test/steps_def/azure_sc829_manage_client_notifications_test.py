import logging
import re
from types import SimpleNamespace

import allure
import pytest
from pytest_bdd import given, parsers, then, when

from default_config import ENVIRONMENT
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.jenkins_client_setup import create_clients_using_jenkins
from utils.api_utils.helper.payload_setup import sc829_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario
from utils.sqlite.SqliteConnection import SqliteConnection

dot_xml_pattern = SimpleNamespace(**search_pattern)


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - CMS updates the client notification successfully
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("CMS updates the client notification successfully")
def test_sc829_updates_client_notification_successfully():
    """CMS updates the client notification successfully"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - CMS returns no notification to update when the notification already exists as active
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("CMS returns no notification to update when the notification already exists as active")
def test_sc829_returns_no_notification_to_update_existing_active_notification():
    """CMS returns no notification to update when the notification already exists as active"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - CMS returns no notification to update when end date is sent but no active notification exists
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("CMS returns no notification to update when end date is sent but no active notification exists")
def test_sc829_returns_no_notification_to_update_end_date_no_active_notification():
    """CMS returns no notification to update when end date is sent but no active notification exists"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - CMS returns invalid request when request-level details are invalid
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("CMS returns invalid request when request-level details are invalid")
def test_sc829_returns_invalid_request():
    """CMS returns invalid request when request-level details are invalid"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - CMS returns client not recognised when the client identifier does not exist in CMS
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("CMS returns client not recognised when the client identifier does not exist in CMS")
def test_sc829_returns_client_not_recognised():
    """CMS returns client not recognised when the client identifier does not exist in CMS"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 6 - CMS returns transaction unsuccessful when CMS business validation fails
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("CMS returns transaction unsuccessful when CMS business validation fails")
def test_sc829_returns_transaction_unsuccessful_when_business_validation_fails():
    """CMS returns transaction unsuccessful when CMS business validation fails"""


@pytest.mark.skip
# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 7 - CMS creates notification successfully using a newly created Jenkins client
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("CMS creates notification successfully using a newly created Jenkins client")
def test_sc829_creates_notification_using_jenkins_client():
    """CMS creates notification successfully using a newly created Jenkins client"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I retrieve a new CMS clients", target_fixture="jenkins_client_id")
def get_cms_client():
    client = None
    try:
        db = SqliteConnection()
        db.connect()
        identifier = {"ENV": ENVIRONMENT, "Notification_created": "FALSE"}
        for i in range(5):
            if client is not None:
                break
            result = db.get_data(table_name="sc829", column_names_and_values=identifier)
            client = result[1]
        db.update_data(
            table_name="sc829",
            data_identifier={"ENV": ENVIRONMENT, "SWN": client},
            new_data={"Notification_created": "TRUE"}
        )
        db.close()
    except Exception as e:
        logging.error(f"An error has occurred when querying the DB: {e}... Creating clients using Jenkins instead")
        if client is None:
            client = create_clients_using_jenkins

        assert client, "Jenkins did not return client ID for IIB."

    return client


@given(
    parsers.parse(
        'I create a valid SC829 manageNotification payload for "{consumer_system}" using the Jenkins-created client '
        'with notification category "{category_code}" and type "{type_code}"'
    ),
    target_fixture="payload"
)
def create_sc829_payload_using_jenkins_client(consumer_system, category_code, type_code, jenkins_client_id):
    return sc829_payload_setup(
        system=consumer_system,
        conditions="correct",
        category_code=category_code,
        type_code=type_code,
        client_identifier=jenkins_client_id
    )


@given(
    parsers.parse(
        'I create a valid SC829 manageNotification payload for "{consumer_system}" '
        'with notification category "{category_code}" and type "{type_code}"'
    ),
    target_fixture="payload"
)
def create_valid_sc829_payload(consumer_system, category_code, type_code):
    return sc829_payload_setup(
        system=consumer_system, conditions="correct", category_code=category_code, type_code=type_code
    )


@given("the client exists in CMS")
def verify_client_exists_precondition(payload):
    """
    Pre-condition step.

    The actual valid client should be supplied from SC829 test data.
    This step only confirms that a payload has been created for the scenario.
    """
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


@given(
    parsers.parse('I create a valid SC829 manageNotification payload for scenario "{scenario_key}"'),
    target_fixture="payload"
)
def create_valid_sc829_payload_for_scenario_key(scenario_key):
    return sc829_payload_setup(scenario_key=scenario_key, conditions="correct")


@given("the same notification state already exists for the client")
def verify_same_notification_state_precondition(payload):
    assert payload["request_body"] is not None


@given(
    parsers.parse('I create an SC829 manageNotification payload with client identifier "{client_identifier}"'),
    target_fixture="payload"
)
def create_sc829_payload_with_client_identifier(client_identifier):
    actual_client_identifier = None if client_identifier == "VALID_CLIENT" else client_identifier

    return sc829_payload_setup(
        system="STAR",
        conditions="correct",
        category_code="STAFFSECURITYALERT",
        type_code="TREP",
        client_identifier=actual_client_identifier
    )


@given(
    parsers.parse(
        "I create an SC829 manageNotification payload with unrecognised client identifier "
        '"{client_identifier}" and identity type "{identity_type}"'
    ),
    target_fixture="payload"
)
def create_sc829_payload_with_unrecognised_client(identity_type):
    return sc829_payload_setup(scenario_key="client_not_recognised", conditions="correct", identity_type=identity_type)


@given(parsers.parse('the payload contains notification category "{category_code}" and type "{type_code}"'))
def update_payload_with_category_and_type(payload, category_code, type_code):
    body = payload["request_body"]

    # Update category code
    if category_code:
        body = re.sub(
            r"(<v15:category>\s*<v14:code>)(.*?)(</v14:code>)",
            rf"\g<1>{category_code}\g<3>",
            body,
            count=1,
            flags=re.DOTALL
        )

    # Missing type scenario: keep type block and blank out notification type code
    if type_code in ("", "MISSING_TYPE"):
        body = re.sub(
            r"(<v13:notification>.*?<v15:type>\s*<v14:code>)(.*?)(</v14:code>)",
            r"\g<1>\g<3>",
            body,
            count=1,
            flags=re.DOTALL
        )

    # Invalid type scenario: update notification type code only
    else:
        body = re.sub(
            r"(<v13:notification>.*?<v15:type>\s*<v14:code>)(.*?)(</v14:code>)",
            rf"\g<1>{type_code}\g<3>",
            body,
            count=1,
            flags=re.DOTALL
        )

    payload["request_body"] = body


@given(parsers.parse('the payload contains start date "{start_date}" and expected end date "{expected_end_date}"'))
def update_payload_dates(payload, start_date, expected_end_date):
    body = payload["request_body"]

    body = re.sub(
        r"(<v14:startDate>)(.*?)(</v14:startDate>)", rf"\g<1>{start_date}\g<3>", body, count=1, flags=re.DOTALL
    )

    body = re.sub(
        r"(<v15:expectedEndDate>)(.*?)(</v15:expectedEndDate>)",
        rf"\g<1>{expected_end_date}\g<3>",
        body,
        count=1,
        flags=re.DOTALL
    )

    payload["request_body"] = body


@given("the same active notification already exists for the client")
def verify_same_active_notification_exists(payload):
    """
    Pre-condition step.
    The test data should already be set up so the same active notification exists in CMS.
    """
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


@given("no active notification exists for the category and type")
def verify_no_active_notification_exists(payload):
    """
    Pre-condition step.
    The test data should already be set up so no active matching notification exists in CMS.
    """
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


@given(parsers.parse('the payload contains end date "{end_date}" only'))
def update_payload_with_end_date_only(payload, end_date):
    body = payload["request_body"]

    # Remove startDate
    body = re.sub(r"<v14:startDate>.*?</v14:startDate>", "", body, count=1, flags=re.DOTALL)

    # Replace existing endDate if present
    if "<v14:endDate>" in body:
        body = re.sub(r"(<v14:endDate>)(.*?)(</v14:endDate>)", rf"\g<1>{end_date}\g<3>", body, count=1, flags=re.DOTALL)
    else:
        # Add endDate inside effective block
        body = re.sub(
            r"(<v15:effective>)(.*?)(</v15:effective>)",
            rf"\g<1><v14:endDate>{end_date}</v14:endDate>\g<3>",
            body,
            count=1,
            flags=re.DOTALL
        )

    payload["request_body"] = body


@given("the expected end date is earlier than the start date")
def verify_expected_end_date_precondition(payload):
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC829 request to the endpoint", target_fixture="response")
def send_sc829_request(api_client, payload):
    endpoint = build_api_endpoint("SC829", system="AZURE")

    response = api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])

    # print("SC829 raw response:")
    # print(response)

    return response


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then('I can see the "Transaction Successful" response returned')
def verify_transaction_successful(api_client, response):
    response_text = response[0] if isinstance(response, tuple) else str(response)

    # print("Response text before XML validation:")
    # print(response_text)

    assert response_text is not None, "Response body is None."
    assert str(response_text).strip().startswith("<"), f"Expected SOAP XML response, but received: {response_text}"

    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, "Transaction Successful")


@then("I can see the SOAP response returned")
def verify_soap_response_returned(response):
    assert response is not None


@then(parsers.parse('I see the result code "{result_code}" returned in the response SOAP'))
def verify_sc829_result_code(api_client, response, result_code):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I see the result message "{message}" returned in the response SOAP'))
def verify_sc829_result_message(api_client, response, message):
    api_client.check_value_in_xml_response(response, dot_xml_pattern.status_message, message)


@then(parsers.parse('I see the subresult message contains "{subresult_message}"'))
def verify_sc829_subresult_message_contains(api_client, response, subresult_message):
    api_client.check_value_in_xml_response(
        response, dot_xml_pattern.subresult_message, subresult_message, is_check_equal=False
    )
