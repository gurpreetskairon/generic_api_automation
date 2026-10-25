import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import int097_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare INT097 successful response
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4619",
    "API-4619",
)
@scenario("Compare INT097 successful response between IIB and Azure")
def test_compare_int097_successful_response():
    """Compare INT097 successful response between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare INT097 unsuccessful responses
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4619",
    "API-4619",
)
@scenario("Compare INT097 unsuccessful response between IIB and Azure")
def test_compare_int097_unsuccessful_response():
    """Compare INT097 unsuccessful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse("I create the INT097 api payload for {condition}"),
    target_fixture="payload",
)
def create_payload(condition):
    return int097_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when("I send INT097 request to IIB endpoint", target_fixture="response_iib")
def send_iib_request(api_client, payload):
    endpoint = build_api_endpoint("INT097", system="IIB")

    if payload["condition"] == "successful_transaction":
        request_body = payload["iib_request_body"]
    else:
        request_body = payload["request_body"]

    return api_client.send_post_request(
        endpoint,
        headers=payload["header"],
        payload=request_body,
        raise_error=False,
    )

@when("I send INT097 request to Azure endpoint", target_fixture="response_azure")
def send_azure_request(api_client, payload):
    endpoint = build_api_endpoint("INT097", system="AZURE")

    if payload["condition"] == "successful_transaction":
        request_body = payload["azure_request_body"]
    else:
        request_body = payload["request_body"]

    return api_client.send_post_request(
        endpoint,
        headers=payload["header"],
        payload=request_body,
        raise_error=False,
    )

# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for INT097")
def validate_response(
    api_client,
    response_iib,
    response_azure,
    payload,
):
    if payload["condition"] == "successful_transaction":
        api_client.compare_soap_responses(
            response_iib,
            response_azure,
            "INT097",
            ignore_tags=["swn"],
        )

    else:
        api_client.compare_soap_responses(
            response_iib,
            response_azure,
            "INT097",
        )
