import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.payload_setup import build_api_endpoint, sc827_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare successful Register Client response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2846", "User Story")
@scenario("Compare SC827 successful Register Client response between Azure and IIB")
def test_compare_sc827_successful_register_client_response_between_azure_and_iib():
    """Compare SC827 successful Register Client response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare unsuccessful Register Client response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2846", "User Story")
@scenario("Compare SC827 unsuccessful Register Client response between Azure and IIB")
def test_compare_sc827_unsuccessful_register_client_response_between_azure_and_iib():
    """Compare SC827 unsuccessful Register Client response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse('I create the correct SC827 comparison payload for "{condition}"'), target_fixture="payload")
def create_correct_sc827_comparison_payload(condition):
    azure_payload = sc827_payload_setup(condition=condition)
    iib_payload = sc827_payload_setup(condition=condition)

    allure.attach(
        azure_payload["request_body"],
        name=f"SC827 Azure comparison request payload - {condition}",
        attachment_type=allure.attachment_type.XML
    )
    allure.attach(
        iib_payload["request_body"],
        name=f"SC827 IIB comparison request payload - {condition}",
        attachment_type=allure.attachment_type.XML
    )
    allure.attach(
        str(azure_payload["header"]),
        name=f"SC827 Azure comparison request headers - {condition}",
        attachment_type=allure.attachment_type.TEXT
    )
    allure.attach(
        str(iib_payload["header"]),
        name=f"SC827 IIB comparison request headers - {condition}",
        attachment_type=allure.attachment_type.TEXT
    )

    return {"condition": condition, "azure_payload": azure_payload, "iib_payload": iib_payload}


@given(parsers.parse('I create the SC827 comparison payload for "{condition}"'), target_fixture="payload")
def create_sc827_comparison_payload_for_condition(condition):
    azure_payload = sc827_payload_setup(condition=condition)
    iib_payload = sc827_payload_setup(condition=condition)

    allure.attach(
        azure_payload["request_body"],
        name=f"SC827 Azure comparison request payload - {condition}",
        attachment_type=allure.attachment_type.XML
    )
    allure.attach(
        iib_payload["request_body"],
        name=f"SC827 IIB comparison request payload - {condition}",
        attachment_type=allure.attachment_type.XML
    )
    allure.attach(
        str(azure_payload["header"]),
        name=f"SC827 Azure comparison request headers - {condition}",
        attachment_type=allure.attachment_type.TEXT
    )
    allure.attach(
        str(iib_payload["header"]),
        name=f"SC827 IIB comparison request headers - {condition}",
        attachment_type=allure.attachment_type.TEXT
    )

    return {"condition": condition, "azure_payload": azure_payload, "iib_payload": iib_payload}


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC827 request to both Azure and IIB endpoints", target_fixture="comparison_response")
def send_sc827_request_to_both_azure_and_iib_endpoints(api_client, payload):
    azure_endpoint = build_api_endpoint("SC827", system="AZURE")
    iib_endpoint = build_api_endpoint("SC827", system="IIB")
    azure_payload = payload["azure_payload"]
    iib_payload = payload["iib_payload"]

    iib_response = api_client.send_post_request(
        iib_endpoint, payload=iib_payload["request_body"], headers=iib_payload["header"]
    )
    azure_response = api_client.send_post_request(
        azure_endpoint, payload=azure_payload["request_body"], headers=azure_payload["header"]
    )

    iib_response_body, _ = api_client.get_response_body_and_status(iib_response, "SC827 IIB")
    azure_response_body, _ = api_client.get_response_body_and_status(azure_response, "SC827 Azure")

    allure.attach(iib_response_body, name="SC827 IIB response", attachment_type=allure.attachment_type.XML)
    allure.attach(azure_response_body, name="SC827 Azure response", attachment_type=allure.attachment_type.XML)

    return {"iib_response": iib_response, "azure_response": azure_response, "payload": payload}


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see the responses are identical")
def validate_response(api_client, comparison_response):
    ignore_tags = ["transactionId", "auditId", "clientNumber"]

    condition = comparison_response["payload"]["condition"]

    if condition == "partner_already_has_current_relationship":
        ignore_tags.append("message")

    api_client.compare_soap_responses(
        iib_response=comparison_response["iib_response"][0],
        azure_response=comparison_response["azure_response"][0],
        service_id="SC827",
        ignore_tags=ignore_tags
    )
