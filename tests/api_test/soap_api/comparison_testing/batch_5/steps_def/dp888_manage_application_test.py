import allure
from pytest_bdd import given, parsers, then, when
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp888_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare DP888 successful responses between IIB and Azure for id verification
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3900", "User Story")
@scenario("Compare DP888 successful responses between IIB and Azure for id verification")
def test_compare_dp888_successful_responses_id_verification():
    """Compare DP888 successful responses between IIB and Azure for id verification"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare DP888 successful responses between IIB and Azure for negative scenarios
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3900", "User Story")
@scenario("Compare DP888 successful responses between IIB and Azure for negative scenarios")
def test_compare_dp888_successful_responses_obligations_verification():
    """Compare DP888 successful responses between IIB and Azure for negative scenarios"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse(
        "I create the api payload with {application_consent}, {relationship_confirmation} and "
        "{application_verification} for {condition}"
    ),
    target_fixture="payload"
)
def create_dp888_payload(application_consent, relationship_confirmation, application_verification, condition):
    return dp888_payload_setup(application_consent, relationship_confirmation, application_verification, condition)


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the request to IIB endpoint", target_fixture="response_iib")
def send_dp888_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("DP888", system="IIB", sub_system="MYMSD")
    return api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True
    )


@when("I send the request to Azure endpoint", target_fixture="response_azure")
def send_dp888_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("DP888", system="AZURE")
    return api_client.send_post_request(
        endpoint, headers=payload[0], params=payload[1], payload=payload[2], json_payload=True
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP888")
def compare_dp888_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "DP888")
