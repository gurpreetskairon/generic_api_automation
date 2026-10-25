import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc127_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Successful
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4529",
    "API-4529",
)
@scenario("Compare SC127 successful transaction response")
def test_compare_sc127_successful_response():
    """Compare SC127 successful response between IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - No Obligation Failure
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4529",
    "API-4529",
)
@scenario("Compare SC127 no obligation failure response")
def test_compare_sc127_no_obligation_failure_response():
    """Compare SC127 no obligation failure response between IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse(
        "I create the SC127 api payload for {condition}"
    ),
    target_fixture="payload",
)
def create_sc127_payload(condition):
    return sc127_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when(
    "I send SC127 request to IIB endpoint",
    target_fixture="response_iib",
)
def send_sc127_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint(
        "SC127",
        system="IIB",
    )

    return api_client.send_post_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
    )


@when(
    "I send SC127 request to Azure endpoint",
    target_fixture="response_azure",
)
def send_sc127_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint(
        "SC127",
        system="AZURE",
    )

    return api_client.send_post_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC127")
def compare_sc127_responses(
    api_client,
    response_iib,
    response_azure,
):
    api_client.compare_soap_responses(
        response_iib,
        response_azure,
        "SC127",
    )
