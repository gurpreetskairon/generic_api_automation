import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.payload_setup import dp605_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare successful notify special caution response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3017", "User Story")
@scenario("Compare DP605 successful notify special caution response between Azure and IIB")
def test_compare_dp605_successful_notify_special_caution_response():
    """Compare DP605 successful notify special caution response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare invalid client number response between Azure and IIB
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-3017", "User Story")
@scenario("Compare DP605 invalid client number response between Azure and IIB")
def test_compare_dp605_invalid_client_number_response():
    """Compare DP605 invalid client number response between Azure and IIB"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse(
        'I created the correct DP605 notify special caution payload for STAR with category "{category_code}" and type "{type_code}"'
    ),
    target_fixture="payload"
)
def create_dp605_notify_special_caution_payload(category_code, type_code):
    return {"category_code": category_code, "type_code": type_code, "condition": "valid_client"}


@given("I used a valid client number as the DP605 path parameter")
def use_valid_client_number_as_dp605_path_parameter(payload):
    payload["condition"] = "valid_client"


@given("I used an invalid client number as the DP605 path parameter")
def use_invalid_client_number_as_dp605_path_parameter(payload):
    payload["condition"] = "invalid_client_number"


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send the DP605 notify special caution request to the Azure endpoint", target_fixture="response_azure")
def send_dp605_request_to_azure(api_client, payload):
    azure_payload = dp605_payload_setup(
        condition=payload["condition"],
        category_code=payload["category_code"],
        type_code=payload["type_code"],
        system="AZURE"
    )

    return api_client.send_post_request(
        azure_payload["endpoint_url"],
        payload=azure_payload["request_body"],
        headers=azure_payload["header"],
        json_payload=True
    )


@when("I send the DP605 notify special caution request to the IIB endpoint", target_fixture="response_iib")
def send_dp605_request_to_iib(api_client, payload):
    iib_payload = dp605_payload_setup(
        condition=payload["condition"],
        category_code=payload["category_code"],
        type_code=payload["type_code"],
        system="IIB",
        subsystem="STAR"
    )

    return api_client.send_post_request(
        iib_payload["endpoint_url"],
        payload=iib_payload["request_body"],
        headers=iib_payload["header"],
        json_payload=True
    )


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP605")
def then_i_can_see_all_the_responses_are_identical_for_dp605(api_client, response_iib, response_azure):
    if isinstance(response_iib, str) and isinstance(response_azure, str):
        # Compare invalid client number response between Azure and IIB
        assert response_iib.split(":", 2)[1] == response_azure.split(":", 2)[1]
    else:
        api_client.compare_json_responses(response_iib[0], response_azure[0], "DP605")
