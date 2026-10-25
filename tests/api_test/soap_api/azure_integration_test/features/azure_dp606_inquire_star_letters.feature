@SOAP-API @dp606-integration @star
Feature: Azure Integration - DP606 - Inquire STAR Letters

  As a client
  I want to send SOAP requests to the Azure api and verify the response
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from Azure endpoints and verify with whats on file


  @positive
  Scenario: Check whether the DP606 responses are the same across different endpoints
    Given I create the correct payload
    And   I send the request to the Azure DP606 endpoint
    Then  I see the response status code matches the expected code 200


  @negative
  Scenario Outline: Check DP606 responses are the same across different endpoints with different conditions
    Given I create the payload with <conditions>
    And   I send the request to the Azure DP606 endpoint
    Then  I see the response status code matches the expected code <status>

    Examples:
      | conditions              | status |
      | missing transactionId   | 500    |
      | missing sourceSystem    | 500    |
      | invalid sourceSystem    | 200    |
      | missing requestDateTime | 500    |
      | invalid client          | 200    |
      | missing client          | 500    |
      | missing auditID         | 500    |


  @negative
  Scenario Outline: Check DP606 responses with unsupported methods
    Given I create the correct payload
    And   I send the request to the Azure DP606 with <method>
    Then  I see the response status code matches the expected code <status>

    Examples:
      | method | status |
      | POST   | 500    |
      | PUT    | 405    |
