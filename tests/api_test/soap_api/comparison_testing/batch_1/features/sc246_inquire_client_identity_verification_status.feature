@SOAP-API
@sc246-comparison
Feature: Comparison Testing - SC246 - Inquire Client Identity Verification Status

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario: Compare SC246 successful response
    Given I create the correct api payload
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical


  @positive
  Scenario Outline: Compare SC246 responses for client with no id verification
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions               |
      | no_identity_verification |


  @negative
  Scenario Outline: Compare SC246 responses with invalid data
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions            |
      | no_matching_client    |
      | invalid_client_number |
      | user_not_recognised   |


  @negative
  Scenario Outline: Compare SC246 responses with invalid header values
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions            |
      | invalid_sourcesystem  |
      | invalid_transactionid |
      | invalid_securitytoken |
