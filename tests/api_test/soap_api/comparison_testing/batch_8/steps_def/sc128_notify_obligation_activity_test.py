
import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc128_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Successful Transaction (12800)
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4528",
    "API-4528",
)
@scenario("Compare SC128 successful transaction response")
def test_compare_sc128_successful_response():
    """Compare SC128 successful response between IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Existing Obligation Failure (12802)
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4528",
    "API-4528",
)
@scenario("Compare SC128 existing obligation failure response")
def test_compare_sc128_existing_obligation_failure_response():
    """Compare SC128 existing obligation failure response between IIB and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse("I create the SC128 api payload for {condition}"),
    target_fixture="payload",
)
def create_sc128_payload(condition):
    return sc128_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when(
    "I send SC128 request to IIB endpoint",
    target_fixture="response_iib",
)
def send_sc128_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint(
        "SC128",
        system="IIB",
    )

    return api_client.send_post_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
    )


@when(
    "I send SC128 request to Azure endpoint",
    target_fixture="response_azure",
)
def send_sc128_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint(
        "SC128",
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
@then("I can see all the responses are identical for SC128")
def compare_sc128_responses(
    api_client,
    response_iib,
    response_azure,
):
    api_client.compare_soap_responses(
        response_iib,
        response_azure,
        "SC128",
        ignore_tags=["eventId", "whenChanged"],
    )
