import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import dp162_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Successful
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4618",
    "API-4618",
)
@scenario("Compare DP162 successful response between DataPower and Azure")
def test_compare_dp162_successful_response():
    """Compare DP162 successful response between DataPower and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Unsuccessful
# ══════════════════════════════════════════════════════════════════════════════
@allure.testcase(
    "https://msd-jira-cloud.atlassian.net/browse/API-4618",
    "API-4618",
)
@scenario("Compare DP162 unsuccessful response between DataPower and Azure")
def test_compare_dp162_unsuccessful_response():
    """Compare DP162 unsuccessful response between DataPower and Azure."""


# ══════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════
@given(
    parsers.parse(
        "I create the DP162 api payload for {condition}"
    ),
    target_fixture="payload",
)
def create_dp162_payload(condition):
    return dp162_payload_setup(condition=condition)


# ══════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════
@when(
    "I send DP162 request to DataPower endpoint",
    target_fixture="response_datapower",
)
def send_dp162_request_to_datapower(api_client, payload):
    endpoint = build_api_endpoint(
        "DP162",
        system="IIB",
        sub_system="MYMSD",
    )

    endpoint = endpoint.replace(
        "{participantId}",
        payload["participant_id"],
    )

    return api_client.send_rest_put_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
        raise_error=payload["raise_error"],
    )


@when(
    "I send DP162 request to Azure endpoint",
    target_fixture="response_azure",
)
def send_dp162_request_to_azure(api_client, payload):
    endpoint = build_api_endpoint(
        "DP162",
        system="AZURE",
    )

    endpoint = endpoint.replace(
        "{participantId}",
        payload["participant_id"],
    )

    return api_client.send_rest_put_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
        raise_error=payload["raise_error"],
    )


# ══════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for DP162")
def compare_dp162_responses(
    api_client,
    response_datapower,
    response_azure,
):
    api_client.compare_json_responses(
        response_datapower,
        response_azure,
        "DP162",
    )
