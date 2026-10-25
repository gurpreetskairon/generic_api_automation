@SOAP-API
Feature: Comparison Testing - DP606 - Inquire STAR Letters

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario: Check whether the DP606 responses are the same across different endpoints
    Given I create the correct api payload
    And   I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see the responses are identical for <response_type>
        | response_type |
        | json          |


  @negative
  Scenario Outline: Check DP606 responses are the same across different endpoints with different conditions
    Given I create the api payload with different <conditions>
    And   I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see the responses are identical for <response_type>

    Examples:
      | conditions              | response_type |
      | missing transactionId   | error string  |
      | missing auditID         | error string  |
      | missing sourceSystem    | error string  |
      | invalid sourceSystem    | json          |
      | missing requestDateTime | error string  |
      | invalid client          | error string  |
      | missing client          | error string  |
