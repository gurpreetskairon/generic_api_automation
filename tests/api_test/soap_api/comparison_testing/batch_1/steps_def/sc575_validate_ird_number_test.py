import allure
from pytest_bdd import given, parsers, then, when

from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.api_utils.helper.payload_setup import sc575_payload_setup
from utils.bdd_utils.scenario import scenario


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 1 - Compare SC575 successful Match response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Compare SC575 successful Match response")
def test_compare_sc575_successful_match_response():
    """Compare SC575 successful Match response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 2 - Compare SC575 No match response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Compare SC575 No match response")
def test_compare_sc575_no_match_response():
    """Compare SC575 No match response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 3 - Compare SC575 transactionId validation response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Compare SC575 transactionId validation response")
def test_compare_sc575_transaction_id_validation_response():
    """Compare SC575 transactionId validation response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 4 - Compare SC575 request parameter validation response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Compare SC575 request parameter validation response")
def test_compare_sc575_request_parameter_validation_response():
    """Compare SC575 request parameter validation response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Scenario 5 - Compare SC575 invalid IRD validation response
# ══════════════════════════════════════════════════════════════════════════════════════
@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-2845", "User Story")
@scenario("Compare SC575 invalid IRD validation response")
def test_compare_sc575_invalid_ird_validation_response():
    """Compare SC575 invalid IRD validation response"""


# ══════════════════════════════════════════════════════════════════════════════════════
# Given steps
# ══════════════════════════════════════════════════════════════════════════════════════
@given("I create an SC575 payload with valid IRD, name, date of birth and address", target_fixture="payload")
def create_sc575_match_payload():
    return sc575_payload_setup(conditions="match")


@given("I create an SC575 payload with a valid IRD", target_fixture="payload")
def create_sc575_valid_ird_payload():
    return sc575_payload_setup(conditions="match")


@given(parsers.parse('I update the payload with a non-matching "{field}"'), target_fixture="payload")
def update_sc575_payload_with_non_matching_field(field):
    if field == "name":
        return sc575_payload_setup(conditions="no_match_name")

    if field == "dateOfBirth":
        return sc575_payload_setup(conditions="no_match_dateOfBirth")

    raise ValueError(f"Unsupported SC575 non-matching field: {field}")


@given(parsers.parse('I create an SC575 payload with "{transaction_id_condition}"'), target_fixture="payload")
def create_sc575_transaction_id_payload(transaction_id_condition):
    return sc575_payload_setup(conditions=transaction_id_condition)


@given(
    parsers.parse('I create an SC575 payload with invalid or missing "{field}" using "{condition}"'),
    target_fixture="payload"
)
def create_sc575_invalid_or_missing_payload(field, condition):
    return sc575_payload_setup(field=field, conditions=condition)


@given(
    "I create an SC575 payload with a 9 digit IRD number that is not valid or does not match the customer type",
    target_fixture="payload"
)
def create_sc575_invalid_customer_type_ird_payload():
    return sc575_payload_setup(conditions="invalid_customer_type_ird")


# ══════════════════════════════════════════════════════════════════════════════════════
# When steps
# ══════════════════════════════════════════════════════════════════════════════════════
@when("I send SC575 request to IIB endpoint", target_fixture="response_iib")
def send_sc575_iib_request(api_client, payload):
    endpoint = build_api_endpoint("SC575", system="IIB")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


@when("I send SC575 request to Azure endpoint", target_fixture="response_azure")
def send_sc575_azure_request(api_client, payload):
    endpoint = build_api_endpoint("SC575", system="AZURE")
    return api_client.send_post_request(endpoint, payload=payload["request_body"], headers=payload["header"])


# ══════════════════════════════════════════════════════════════════════════════════════
# Then steps
# ══════════════════════════════════════════════════════════════════════════════════════
@then("I can see all the responses are identical for SC575")
def then_i_can_see_all_the_responses_are_identical_for_sc575(api_client, response_iib, response_azure):
    api_client.compare_soap_responses(response_iib, response_azure, "SC575", ignore_element_order=True)
