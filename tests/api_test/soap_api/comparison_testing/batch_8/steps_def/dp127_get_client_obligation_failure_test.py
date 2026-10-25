import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp127_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Successful
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4530",
    "API-4530",
)
@scenario("Compare DP127 successful transaction response")
def test_compare_dp127_successful_response():
    """Compare DP127 successful response between IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - No Obligation Failure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4530",
    "API-4530",
)
@scenario("Compare DP127 no obligation failure response")
def test_compare_dp127_no_obligation_failure_response():
    """Compare DP127 no obligation failure response between IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse("I create the DP127 api request for {condition}"),
    target_fixture="payload",
)
def create_dp127_payload(condition):
    return dp127_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when(
    "I send DP127 request to IIB endpoint",
    target_fixture="response_iib",
)
def send_dp127_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint(
        "DP127",
        system="IIB",
        sub_system="MYMSD",
    )

    return api_client.send_get_request(
        endpoint,
        params=payload["params"],
        headers=payload["header"],
    )


@when(
    "I send DP127 request to Azure endpoint",
    target_fixture="response_azure",
)
def send_dp127_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint(
        "DP127",
        system="AZURE",
    )

    return api_client.send_get_request(
        endpoint,
        params=payload["params"],
        headers=payload["header"],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP127")
def compare_dp127_responses(
    api_client,
    response_iib,
    response_azure,
):
    api_client.compare_json_responses(
        response_iib,
        response_azure,
        "DP127",
    )
