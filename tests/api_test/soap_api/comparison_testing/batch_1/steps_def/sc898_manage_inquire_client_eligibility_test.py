import os

import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc898_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare successful Click to Enrol eligibility response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3060", "User Story")
@scenario("Compare SC898 successful Click to Enrol eligibility response between Azure and IIB")
def test_compare_sc898_successful_click_to_enrol_eligibility_response_between_azure_and_iib():
    """Compare SC898 successful Click to Enrol eligibility response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare negative business response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3060", "User Story")
@scenario("Compare SC898 negative business response between Azure and IIB")
def test_compare_sc898_negative_business_response_between_azure_and_iib():
    """Compare SC898 negative business response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare missing client number exception response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3060", "User Story")
@scenario("Compare SC898 missing client number exception response between Azure and IIB")
def test_compare_sc898_missing_client_number_exception_response_between_azure_and_iib():
    """Compare SC898 missing client number exception response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I created the correct SC898 api payload for {client_flag_condition}"), target_fixture="payload")
def create_correct_sc898_payload_for_client_flag_condition(client_flag_condition):
    return sc898_payload_setup(client_flag_condition)


@given(parsers.parse("I created the SC898 api payload for {negative_condition}"), target_fixture="payload")
def create_sc898_payload_for_negative_condition(negative_condition):
    return sc898_payload_setup(negative_condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC898 request to both Azure and IIB endpoints", target_fixture="responses")
def send_sc898_request_to_both_azure_and_iib_endpoints(api_client, payload):
    azure_endpoint = build_api_endpoint("SC898", system="AZURE")
    iib_endpoint = build_api_endpoint("SC898", system="IIB")

    if os.getenv("ENVIRONMENT_NAME", "").casefold() == "sit":
        azure_endpoint = azure_endpoint.replace("dev", "sit")
        iib_endpoint = iib_endpoint.replace("dev", "sit")

    azure_response = api_client.send_post_request(
        azure_endpoint, payload=payload["request_body"], headers=payload["header"]
    )
    iib_response = api_client.send_post_request(
        iib_endpoint, payload=payload["request_body"], headers=payload["header"]
    )

    return {"azure_response": azure_response, "iib_response": iib_response}


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC898")
def then_i_can_see_all_the_responses_are_identical_for_sc898(api_client, responses):
    api_client.compare_soap_responses(
        responses["iib_response"],
        responses["azure_response"],
        "SC898",
        ignore_element_order=True,
        ignore_tags=["correlationId"]
    )
