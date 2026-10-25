import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc532_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC532V2 successful and filtered responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3622", "User Story")
@scenario("Compare SC532V2 successful and filtered responses")
def test_compare_sc532v2_successful_and_filtered_responses():
    """Compare successful and filtered SC532V2 responses returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC532V2 no active product delivery response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3622", "User Story")
@scenario("Compare SC532V2 no active product delivery response")
def test_compare_sc532v2_no_active_product_delivery_response():
    """Compare the SC532V2 no-active-product-delivery response returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC532V2 unsuccessful responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3622", "User Story")
@scenario("Compare SC532V2 unsuccessful responses")
def test_compare_sc532v2_unsuccessful_responses():
    """Compare unsuccessful SC532V2 responses returned by IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC532V2 api payload for {condition}"), target_fixture="payload")
def create_sc532v2_payload_for_condition(condition):
    return sc532_payload_setup(condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send SC532V2 get product delivery details request to IIB endpoint", target_fixture="response_iib")
def send_sc532v2_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC532", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC532V2 get product delivery details request to Azure endpoint", target_fixture="response_azure")
def send_sc532v2_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC532", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC532V2")
def compare_sc532v2_responses(api_client, response_iib, response_azure):
    (
        api_client.compare_soap_responses(
            response_iib,
            response_azure,
            "SC532",
            ignore_element_order=True,
            ignore_tags=["registrationDate", "startDate", "commencementDate", "renewalDate", "expiryDate"]
        )
    )
