import allure
from pytest_bdd import given, parsers, then, when
from apps.services.integration_soap.payload_data.sc862 import update_sc862_endpoint
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc862_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC862 successful response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4130", "User Story")
@scenario("Compare SC862 successful responses between IIB and Azure")
def test_compare_sc862_successful_responses():
    """Compare SC862 successful responses between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC862 negative response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-4130", "User Story")
@scenario("Compare SC862 negative response between IIB and Azure")
def test_compare_sc862_negative_responses():
    """Compare SC862 negative response between IIB and Azure"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(parsers.parse("I create the SC862 api payload for {condition}"), target_fixture="payload")
def create_sc862_payload(condition):
    return sc862_payload_setup(condition=condition), condition


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC862 request to IIB endpoint", target_fixture="response_iib")
def send_sc862_request_to_iib(api_client, payload):
    endpoint = build_api_endpoint("SC862", system="IIB")
    endpoint = update_sc862_endpoint(endpoint, payload[1])
    return api_client.send_get_request(endpoint, params=payload[0][1], headers=payload[0][0], raise_on_error=False)


@when("I send SC862 request to Azure endpoint", target_fixture="response_azure")
def send_sc862_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint("SC862", system="AZURE")
    endpoint = update_sc862_endpoint(endpoint, payload[1])
    return api_client.send_get_request(endpoint, params=payload[0][1], headers=payload[0][0], raise_on_error=False)


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC862")
def compare_sc862_responses(api_client, response_iib, response_azure):
    api_client.compare_json_responses(response_iib, response_azure, "SC862")
