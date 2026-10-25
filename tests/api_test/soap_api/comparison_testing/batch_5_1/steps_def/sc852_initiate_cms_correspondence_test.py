from uuid import uuid4

import allure
import pytest
from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.common_utils.helper_functions.xml_parser import replace_tag_value
from utils.api_utils.helper.payload_setup import sc852_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC852 successful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4325",
    "User Story",
)
@scenario("Compare SC852 successful transaction response")
def test_compare_sc852_successful_transaction_response():
    """Compare SC852 successful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC852 unsuccessful transaction response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4325",
    "User Story",
)
@scenario("Compare SC852 unsuccessful transaction response")
def test_compare_sc852_unsuccessful_transaction_response():
    """Compare SC852 unsuccessful transaction response."""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse(
        "I create the correct SC852 api payload with different {conditions}"
    ),
    target_fixture="payload",
)
def create_sc852_payload_with_condition(conditions):
    return sc852_payload_setup(conditions)


@given(
    "I send the SC852 request to IIB endpoint",
    target_fixture="response_iib",
)
def send_sc852_request_to_iib_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC852", system="IIB")

    request_body = payload["request_body"]

    if payload["condition"] == "successful_response":
        request_body = replace_tag_value(
            request_body,
            "transactionId",
            str(uuid4()),
        )

    return api_client.send_post_request(
        endpoint,
        payload=request_body,
        headers=payload["header"],
    )


@given(
    "I send the SC852 request to Azure endpoint",
    target_fixture="response_azure",
)
def send_sc852_request_to_azure_endpoint(api_client, payload):
    endpoint = build_api_endpoint("SC852", system="AZURE")

    request_body = payload["request_body"]

    if payload["condition"] == "successful_response":
        request_body = replace_tag_value(
            request_body,
            "transactionId",
            str(uuid4()),
        )

    return api_client.send_post_request(
        endpoint,
        payload=request_body,
        headers=payload["header"],
    )

# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC852")
def compare_all_sc852_responses(
    api_client,
    response_iib,
    response_azure,
    payload,
):
    if payload["condition"] == "successful_response":
        api_client.compare_soap_responses(
            response_iib,
            response_azure,
            "SC852",
            ignore_tags=[
                "transactionId",
                "correspondenceId",
                "url",
            ],
        )
    else:
        api_client.compare_soap_responses(
            response_iib,
            response_azure,
            "SC852",
        )
