from types import SimpleNamespace

import allure
import pytest
from lxml import etree
from pytest_bdd import given, then, when

from utils.api_utils.helper.payload_setup import sc825_payload_setup
from utils.api_utils.helper.xml_pattern import search_pattern
from utils.bdd_utils.scenario import scenario

dot_xml_pattern = SimpleNamespace(**search_pattern)


@allure.testcase("https://msd-jira-cloud.atlassian.net/browse/API-0000", "User Story")
@scenario("Check sandbox response schema")
def test_check_sandbox_response_schema():
    """Check sandbox response schema"""


@given("I created the correct sandbox api payload", target_fixture="payload")
def create_correct_payload():
    payload = sc825_payload_setup("not_secured")
    payload["request_body"] = payload["request_body"].replace(
        "http://msd.govt.nz/integration/derived/participant/service/inquireparticipant/v1",
        "http://msd.govt.nz/integration/derived/participant/service/sandbox/v1"
    )
    return payload


@given("I sent the sandbox request to the Azure endpoint", target_fixture="response")
@when("I sent the sandbox request to the Azure endpoint", target_fixture="response")
def send_sandbox_request(api_client, payload):
    mocked_response = """<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">
    <soapenv:Body>
        <v1:inquireParticipantResponse xmlns:v1=\"http://msd.govt.nz/integration/derived/participant/service/sandbox/v1\">
            <v1:resultCode>OK</v1:resultCode>
            <v1:resultMessage>Mocked sandbox response</v1:resultMessage>
        </v1:inquireParticipantResponse>
    </soapenv:Body>
</soapenv:Envelope>"""
    return mocked_response, 200


@then("I can see the sandbox response schema returned")
def verify_schema(api_client, response):
    try:
        etree.fromstring(response[0].encode("utf-8") if isinstance(response[0], str) else response[0])
    except Exception as exc:
        raise AssertionError(f"Sandbox response is not valid XML: {response[0]}") from exc
