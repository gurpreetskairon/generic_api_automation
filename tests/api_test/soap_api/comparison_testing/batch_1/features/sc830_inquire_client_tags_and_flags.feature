@SOAP-API
Feature: Comparison Testing - SC830 - Inquire client tags and flags

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaves like-for-like with IIB

  Acceptance:
  * IIB and Azure responses are identical for the agreed SC830 comparison scenarios

  Notes:
  * Detailed validation of result code, result message, subresult, programme tag details and client flag details is covered under Azure integration testing.
  * Comparison testing sends the same payload to IIB and Azure and validates that both endpoint responses are identical.
  * XML namespace prefixes are not treated as business-data differences.


  @positive
  Scenario: Compare SC830 successful response when client has programme tags and client flags
    Given I create the correct api payload
    When  I send inquire participant request for client tags and flags to IIB endpoint
    And   I send inquire participant request for client tags and flags to Azure endpoint
    Then  I can see all the responses are identical for SC830


  @positive
  Scenario Outline: Compare SC830 successful result and subresult
    Given I create the correct api payload for <client_type>
    When  I send inquire participant request for client tags and flags to IIB endpoint
    And   I send inquire participant request for client tags and flags to Azure endpoint
    Then  I can see all the responses are identical for SC830

    Examples:
      | client_type               |
      | no_current_programme_tags |
      | no_current_flags          |


  @negative
  Scenario Outline: Compare SC830 responses when the client or user cannot be validated
    Given I create the api payload for <condition>
    When  I send inquire participant request for client tags and flags to IIB endpoint
    And   I send inquire participant request for client tags and flags to Azure endpoint
    Then  I can see all the responses are identical for SC830

    Examples:
      | condition             |
      | no_matching_client    |
      | invalid_client_number |
      | missing_client_number |
      | user_not_recognised   |
