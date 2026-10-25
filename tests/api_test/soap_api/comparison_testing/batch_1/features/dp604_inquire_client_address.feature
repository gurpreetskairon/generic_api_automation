@SOAP-API
Feature: Comparison Testing - DP604 - Inquire Client Address

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario: Check whether the DP604 responses are the same across different endpoints
    Given I create the correct api payload
    And   I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for DP604


  @negative
  Scenario Outline: Check DP604 responses are the same across different endpoints with different conditions
    Given I create the api payload with different <conditions>
    And   I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for DP604

    Examples:
      | conditions              |
      | missing authorization   |
      | invalid authorization   |
      | missing transactionId   |
      | invalid transactionId   |
      | missing sourceSystem    |
      | invalid sourceSystem    |
      | invalid requestDateTime |
      | missing securityTokenId |
      | invalid securityTokenId |
      | unencoded clientID      |
      | invalid clientID        |


  @negative
  Scenario Outline: Check DP604 responses are the same across different endpoints with different jws
    Given I create the api payload with different <conditions>
    And   I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for DP604

    Examples:
      | conditions            |
      | missing jws           |
      | invalid jws key       |
      | invalid jws algorithm |
      | invalid jws method    |
      | invalid query string  |
