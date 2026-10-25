import os

import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc847_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare successful Drug Test Referral Delay response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3150", "User Story")
@scenario("Compare SC847 successful Drug Test Referral Delay response between Azure and IIB")
def test_compare_sc847_successful_drug_test_referral_delay_response_between_azure_and_iib():
    """Compare SC847 successful Drug Test Referral Delay response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC847 no matching record response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3150", "User Story")
@scenario("Compare SC847 no matching record response between Azure and IIB")
def test_compare_sc847_no_matching_record_response_between_azure_and_iib():
    """Compare SC847 no matching record response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I created the correct SC847 api payload for {dtrd_condition}"), target_fixture="payload")
def create_correct_sc847_payload_for_dtrd_condition(dtrd_condition):
    return sc847_payload_setup(dtrd_condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the SC847 request to both Azure and IIB endpoints", target_fixture="responses")
def send_sc847_request_to_both_azure_and_iib_endpoints(api_client, payload):
    azure_endpoint = build_api_endpoint("SC847", system="AZURE")
    iib_endpoint = build_api_endpoint("SC847", system="IIB")

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
@then("I can see all the responses are identical for SC847")
def then_i_can_see_all_the_responses_are_identical_for_sc847(api_client, responses):
    api_client.compare_soap_responses(
        responses["iib_response"], responses["azure_response"], "SC847", ignore_element_order=True
    )
