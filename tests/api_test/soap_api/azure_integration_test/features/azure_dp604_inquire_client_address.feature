@AZURE-SOAP-API @SOAP-API @dp604-integration @star
Feature: Azure Integration - DP604 - Inquire Client Address

  As a client
  I want to send SOAP requests to the Azure api and verify the response
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from Azure endpoints and verify with whats on file


  @positive
  Scenario Outline: Check whether the DP604 azure responses match whats on file
    Given I create the correct payload
    And   I send the request to the Azure DP604 endpoint
    Then  I see the response matches the <conditions> expected response and <status> on file

    Examples:
      | conditions        | status |
      | positive_scenario | 200    |


  @negative
  Scenario Outline: Check whether the DP604 azure responses match whats on file with varying conditions
    Given I create the payload with <conditions>
    And   I send the request to the Azure DP604 endpoint
    Then  I see the response matches the <conditions> expected response and <status> on file

    Examples:
      | conditions              | status |
      | missing transactionId   | 400    |
      | missing sourceSystem    | 400    |
      | invalid sourceSystem    | 200    |
      | missing requestDateTime | 400    |
      | invalid requestDateTime | 400    |
      | missing securityTokenId | 400    |
      | invalid securityTokenId | 470    |
      | unencoded clientID      | 400    |
      | invalid clientID        | 470    |


  @negative
  Scenario Outline: Check whether the DP604 azure responses match whats on file with varying jws conditions
    Given I create the payload with <conditions>
    And   I send the request to the Azure DP604 endpoint
    Then  I see the response matches the <conditions> expected response and <status> on file

    Examples:
      | conditions            | status |
      | missing jws           | 400    |
      | invalid jws key       | 400    |
      | invalid jws algorithm | 400    |
      | invalid jws method    | 400    |
      | invalid query string  | 400    |
