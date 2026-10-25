import logging
import re
import allure
from pytest_bdd import given, parsers, then, when
from default_config import ENVIRONMENT
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.jenkins_client_setup import create_clients_using_jenkins, create_two_clients_using_jenkins
from utils.api_utils.helper.payload_setup import sc829_payload_setup
from utils.api_utils.helper.xml_pattern import dot_xml_pattern
from utils.bdd_utils.scenario import scenario
from utils.sqlite.SqliteConnection import SqliteConnection


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - IIB and Azure return matching successful transaction response for SC829
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("IIB and Azure return matching successful transaction response for SC829")
def test_sc829_compare_successful_transaction_response():
    """IIB and Azure return matching successful transaction response for SC829"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - No notification to update response when notification already exists as active
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("IIB and Azure return matching no notification to update response when notification already exists as active")
def test_sc829_compare_no_notification_to_update_existing_active_notification():
    """IIB and Azure return matching no notification to update response when notification already exists as active"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - No notification to update response when end date is sent but no active notification exists
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario(
    "IIB and Azure return matching no notification to update response when end date is sent but no active notification exists"
)
def test_sc829_compare_no_notification_to_update_end_date_no_active_notification():
    """IIB and Azure return matching no notification to update response when end date is sent but no active notification exists"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - IIB and Azure return matching invalid request response for SC829
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("IIB and Azure return matching invalid request response for SC829")
def test_sc829_compare_invalid_request_response():
    """IIB and Azure return matching invalid request response for SC829"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - IIB and Azure return matching client not recognised response for SC829
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("IIB and Azure return matching client not recognised response for SC829")
def test_sc829_compare_client_not_recognised_response():
    """IIB and Azure return matching client not recognised response for SC829"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 6 - Return matching transaction unsuccessful response when business validation fails
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
@scenario("IIB and Azure return matching transaction unsuccessful response when business validation fails")
def test_sc829_compare_transaction_unsuccessful_response():
    """IIB and Azure return matching transaction unsuccessful response when business validation fails"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 7 - Return matching successful business outcome using separate Jenkins-created clients
# ══════════════════════════════════════════════════════════════════════════════════════
# @allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2948", "User Story")
# @scenario("IIB and Azure return matching successful business outcome using separate Jenkins-created clients")
# def test_sc829_compare_successful_business_outcome_using_separate_jenkins_clients():
#     """IIB and Azure return matching successful business outcome using separate Jenkins-created clients"""


# ══════════════════════════════════════════════════════════════════════════════════════
# SC829-specific helper functions
# ══════════════════════════════════════════════════════════════════════════════════════
def _replace_xml_value(body, tag_name, new_value):
    pattern = rf"(<[^:/\s>]+:{tag_name}[^>]*>)(.*?)(</[^:/\s>]+:{tag_name}>)"
    return re.sub(pattern, rf"\g<1>{new_value}\g<3>", body, count=1, flags=re.DOTALL)


def _replace_category_code(body, category_code):
    pattern = r"(<[^:/\s>]+:category[^>]*>.*?<[^:/\s>]+:code[^>]*>)(.*?)(</[^:/\s>]+:code>.*?</[^:/\s>]+:category>)"
    return re.sub(pattern, rf"\g<1>{category_code}\g<3>", body, count=1, flags=re.DOTALL)


def _replace_type_code(body, type_code):
    pattern = r"(<[^:/\s>]+:type[^>]*>.*?<[^:/\s>]+:code[^>]*>)(.*?)(</[^:/\s>]+:code>.*?</[^:/\s>]+:type>)"
    return re.sub(pattern, rf"\g<1>{type_code}\g<3>", body, count=1, flags=re.DOTALL)


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I retrieve two new CMS clients", target_fixture="client_ids")
def get_two_cms_clients():
    iib_client_id, azure_client_id = None, None

    try:
        db = SqliteConnection()
        db.connect()

        identifier = {"ENV": ENVIRONMENT, "Notification_created": "FALSE"}

        for _ in range(5):
            if iib_client_id is not None and azure_client_id is not None:
                break

            result = db.get_data(table_name="sc829", column_names_and_values=identifier)

            if iib_client_id is None:
                iib_client_id = result[1]
            elif azure_client_id is None and result[1] != iib_client_id:
                azure_client_id = result[1]

        db.update_data(
            table_name="sc829",
            data_identifier={"ENV": ENVIRONMENT, "SWN": iib_client_id},
            new_data={"Notification_created": "TRUE"}
        )
        db.update_data(
            table_name="sc829",
            data_identifier={"ENV": ENVIRONMENT, "SWN": azure_client_id},
            new_data={"Notification_created": "TRUE"}
        )
        db.close()

    except Exception as error:
        logging.error(f"An error has occurred when querying the DB: {error}. Creating clients using Jenkins instead.")

        if iib_client_id is None and azure_client_id is None:
            iib_client_id, azure_client_id = create_two_clients_using_jenkins()
        elif iib_client_id is None:
            iib_client_id = create_clients_using_jenkins()
        elif azure_client_id is None:
            azure_client_id = create_clients_using_jenkins()

        assert iib_client_id, "Jenkins did not return client ID for IIB."
        assert azure_client_id, "Jenkins did not return client ID for Azure."

    return {"iib_client_id": iib_client_id, "azure_client_id": azure_client_id}


@given(
    parsers.parse(
        'I create a valid SC829 manageNotification payload for "{consumer_system}" using the first Jenkins-created client for IIB with notification category "{category_code}" and type "{type_code}"'
    ),
    target_fixture="iib_payload"
)
def create_iib_payload_using_first_jenkins_client(consumer_system, category_code, type_code, client_ids):
    return sc829_payload_setup(
        system=consumer_system,
        conditions="correct",
        category_code=category_code,
        type_code=type_code,
        client_identifier=client_ids["iib_client_id"]
    )


@given(
    parsers.parse(
        'I create a valid SC829 manageNotification payload for "{consumer_system}" using the second Jenkins-created client for Azure with notification category "{category_code}" and type "{type_code}"'
    ),
    target_fixture="azure_payload"
)
def create_azure_payload_using_second_jenkins_client(consumer_system, category_code, type_code, client_ids):
    return sc829_payload_setup(
        system=consumer_system,
        conditions="correct",
        category_code=category_code,
        type_code=type_code,
        client_identifier=client_ids["azure_client_id"]
    )


@given(
    parsers.parse(
        'I create a valid SC829 manageNotification payload for "{consumer_system}" with notification category "{category_code}" and type "{type_code}"'
    ),
    target_fixture="payload"
)
def create_valid_sc829_payload(consumer_system, category_code, type_code):
    return sc829_payload_setup(
        system=consumer_system, conditions="correct", category_code=category_code, type_code=type_code
    )


@given("the client exists in CMS")
def verify_client_exists_precondition(payload):
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


@given("the same active notification already exists for the client")
def verify_same_active_notification_exists(payload):
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


@given("no active notification exists for the category and type")
def verify_no_active_notification_exists(payload):
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


@given(
    parsers.parse('I create a valid SC829 manageNotification payload for scenario "{scenario_key}"'),
    target_fixture="payload"
)
def create_valid_sc829_payload_for_scenario_key(scenario_key):
    return sc829_payload_setup(scenario_key=scenario_key, conditions="correct")


@given("the same notification state already exists for the client")
def verify_existing_notification_precondition(payload):
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


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
        'I create an SC829 manageNotification payload with unrecognised client identifier "{client_identifier}" and identity type "{identity_type}"'
    ),
    target_fixture="payload"
)
def create_sc829_payload_with_unrecognised_client(client_identifier, identity_type):
    return sc829_payload_setup(
        system="STAR",
        conditions="correct",
        category_code="STAFFSECURITYALERT",
        type_code="TREP",
        client_identifier=client_identifier,
        identity_type=identity_type
    )


@given(parsers.parse('the payload contains notification category "{category_code}" and type "{type_code}"'))
def update_payload_with_category_and_type(api_client, payload, category_code, type_code):
    body = payload["request_body"]

    if category_code:
        body = api_client.replace_xml_child_code_value(body, "category", category_code)

    body = api_client.replace_xml_child_code_value(body, "type", "" if type_code in ("", "MISSING_TYPE") else type_code)
    payload["request_body"] = body


@given(parsers.parse('the payload contains end date "{end_date}" only'))
def update_payload_with_end_date_only(api_client, payload, end_date):
    body = payload["request_body"]
    body = api_client.remove_xml_element(body, "startDate")

    if "<v14:endDate>" in body:
        body = api_client.replace_xml_tag_value(body, "endDate", end_date)
    else:
        body = api_client.add_xml_child_to_parent(body, "effective", f"<v14:endDate>{end_date}</v14:endDate>")

    payload["request_body"] = body


@given(parsers.parse('the payload contains start date "{start_date}" and expected end date "{expected_end_date}"'))
def update_payload_dates(api_client, payload, start_date, expected_end_date):
    body = payload["request_body"]

    if start_date:
        body = api_client.replace_xml_tag_value(body, "startDate", start_date)

    if expected_end_date:
        body = api_client.replace_xml_tag_value(body, "expectedEndDate", expected_end_date)

    payload["request_body"] = body


@given("the expected end date is earlier than the start date")
def verify_expected_end_date_is_earlier_precondition(payload):
    assert payload is not None, "SC829 payload was not created."
    assert payload.get("request_body") is not None, "SC829 request body was not created."


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC829 request to the IIB endpoint", target_fixture="response_iib")
def send_sc829_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC829", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send the same SC829 request to the Azure endpoint", target_fixture="response_azure")
def send_sc829_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC829", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send the SC829 request to the IIB endpoint using the IIB payload", target_fixture="response_iib")
def send_sc829_iib_request_with_iib_payload(api_client, iib_payload):
    endpoint = build_api_endpoint("SC829", system="IIB")
    return api_client.send_post_request(endpoint, payload=iib_payload["request_body"], headers=iib_payload["header"])


@when("I send the SC829 request to the Azure endpoint using the Azure payload", target_fixture="response_azure")
def send_sc829_azure_request_with_azure_payload(api_client, azure_payload):
    endpoint = build_api_endpoint("SC829", system="AZURE")
    return api_client.send_post_request(
        endpoint, payload=azure_payload["request_body"], headers=azure_payload["header"]
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the IIB and Azure responses are identical")
def compare_iib_and_azure_responses_are_identical(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC829", ignore_element_order=True)


@then(parsers.parse('I see the result code "{result_code}" returned in both SOAP responses'))
def verify_result_code_in_both_responses(api_client, response_iib, response_azure, result_code):
    api_client.check_value_in_xml_response(response_iib, dot_xml_pattern.result_code, result_code)
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.result_code, result_code)


@then(parsers.parse('I see the result message "{message}" returned in both SOAP responses'))
def verify_result_message_in_both_responses(api_client, response_iib, response_azure, message):
    api_client.check_value_in_xml_response(response_iib, dot_xml_pattern.status_message, message)
    api_client.check_value_in_xml_response(response_azure, dot_xml_pattern.status_message, message)
