from pytest_bdd import given, parsers, then

from utils.api_utils.helper.api_endpoint_builders import (
    build_api_endpoint,
)
from utils.api_utils.helper.payload_setup import (
    sc152_payload_setup,
    sc152_update_payload_setup,
)
from utils.bdd_utils.scenario import scenario


# ============================================================================
# POST - Successful response
# ============================================================================
@scenario("Compare SC152 successful transaction response")
def test_compare_sc152_successful_transaction_response():
    """Compare SC152 POST successful transaction."""


# ============================================================================
# POST - Invalid request
# ============================================================================
@scenario("Compare SC152 invalid request response")
def test_compare_sc152_invalid_request_response():
    """Compare SC152 POST invalid request."""


# ============================================================================
# PUT - Successful response
# ============================================================================
@scenario("Compare SC152 successful update response")
def test_compare_sc152_successful_update_response():
    """Compare SC152 PUT successful update."""


# ============================================================================
# PUT - Invalid request
# ============================================================================
@scenario("Compare SC152 invalid update response")
def test_compare_sc152_invalid_update_response():
    """Compare SC152 PUT invalid update."""


# ============================================================================
# POST payload
# ============================================================================
@given(
    parsers.parse(
        "I create the correct SC152 api request "
        "with different {conditions}"
    ),
    target_fixture="payload",
)
def create_sc152_request_with_condition(conditions):
    return sc152_payload_setup(conditions)


# ============================================================================
# POST Given steps
# ============================================================================
@given(
    "I send the SC152 request to IIB endpoint",
    target_fixture="response_iib",
)
def send_sc152_request_to_iib_endpoint(
    api_client,
    payload,
):
    endpoint = build_api_endpoint(
        "SC152_CREATE",
        system="IIB",
    ).replace(
        "{action_id}",
        payload["action_id"],
    )

    return api_client.send_post_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
        json_payload=True,
        raise_error=payload["raise_error"],
    )


@given(
    "I send the SC152 request to Azure endpoint",
    target_fixture="response_azure",
)
def send_sc152_request_to_azure_endpoint(
    api_client,
    payload,
):
    endpoint = build_api_endpoint(
        "SC152_CREATE",
        system="AZURE",
    ).replace(
        "{action_id}",
        payload["action_id"],
    )

    return api_client.send_post_request(
        endpoint,
        payload["request_body"],
        headers=payload["header"],
        json_payload=True,
        raise_error=payload["raise_error"],
    )


# ============================================================================
#  POST then steps
# ============================================================================
@then("I can see all the responses are identical for SC152")
def compare_all_sc152_responses(
    api_client,
    response_iib,
    response_azure,
):
    api_client.compare_json_responses(
        response_iib,
        response_azure,
        "SC152",
        exclude_fields=[
            "job_search_activity_id",
        ],
    )


# ============================================================================
# PUT given steps
# ============================================================================
@given(
    parsers.parse(
        "I create the correct SC152 update api request "
        "with different {conditions}"
    ),
    target_fixture="update_payload",
)
def create_sc152_update_request_with_condition(
    conditions,
):
    return sc152_update_payload_setup(conditions)



@given(
    "I send the SC152 update request to IIB endpoint",
    target_fixture="update_response_iib",
)
def send_sc152_update_request_to_iib_endpoint(
    api_client,
    update_payload,
):
    endpoint = build_api_endpoint(
        "SC152_UPDATE",
        system="IIB",
    )

    endpoint = endpoint.replace(
        "{action_id}",
        update_payload["action_id"],
    )

    endpoint = endpoint.replace(
        "{job_search_activity_id}",
        update_payload["job_search_activity_id"],
    )

    return api_client.send_rest_put_request(
        endpoint,
        update_payload["request_body"],
        headers=update_payload["header"],
        raise_error=update_payload["raise_error"],
    )



@given(
    "I send the SC152 update request to Azure endpoint",
    target_fixture="update_response_azure",
)
def send_sc152_update_request_to_azure_endpoint(
    api_client,
    update_payload,
):
    endpoint = build_api_endpoint(
        "SC152_UPDATE",
        system="AZURE",
    )

    endpoint = endpoint.replace(
        "{action_id}",
        update_payload["action_id"],
    )

    endpoint = endpoint.replace(
        "{job_search_activity_id}",
        update_payload["job_search_activity_id"],
    )

    return api_client.send_rest_put_request(
        endpoint,
        update_payload["request_body"],
        headers=update_payload["header"],
        raise_error=update_payload["raise_error"],
    )


# ============================================================================
#  PUT then steps
# ============================================================================
@then(
    "I can see all the SC152 update responses are identical"
)
def compare_sc152_update_responses(
    api_client,
    update_response_iib,
    update_response_azure,
):
    api_client.compare_json_responses(
        update_response_iib,
        update_response_azure,
        "SC152",
    )
