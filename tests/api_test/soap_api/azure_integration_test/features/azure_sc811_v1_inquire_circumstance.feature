@AZURE-SOAP-API @SOAP-API @sc811-v1-integration
Feature: Azure Integration - SC811 V1 - Inquire Circumstance

  As a client
  I want to send SOAP requests to the Azure SC811 V1 endpoint
  So that I can validate the response returned for inquiring client circumstances.

  # SC811 V1 returns historic or current client circumstance details used
  # to determine eligibility and entitlement to Ministry products and services.

  # Test Data Notes
  # - Success (81100): Valid client with matching circumstance data.
  # - No Matching Record (81103): Valid client with no matching circumstances for the request.
  # - Invalid Request (81101): Triggered by an invalid request payload.
  # - Client Not Recognised (81102): Client number is not recognised.


  @positive
  Scenario Outline: Check SC811 V1 successful transaction response
    Given I create the correct payload for SC811 V1 with "<condition>"
    When  I send the SC811 V1 request to the Azure endpoint
    Then  I can see the SC811 V1 result code as "<result_code>"
    And   I can see the SC811 V1 result message as "<result_message>"

    Examples:
      | condition          | result_code | result_message         |
      | success            | 81100       | Transaction Successful |
      | no_matching_record | 81103       | No matching record     |


  @negative
  Scenario Outline: Check SC811 V1 unsuccessful transaction response
    Given I create the payload for SC811 V1 with "<condition>"
    When  I send the SC811 V1 request to the Azure endpoint
    Then  I can see the SC811 V1 result code as "<result_code>"
    And   I can see the SC811 V1 result message as "<result_message>"

    Examples:
      | condition             | result_code | result_message        |
      | invalid_request       | 81101       | Invalid Request       |
      | client_not_recognised | 81102       | Client not recognised |
