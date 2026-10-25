@SOAP-API
Feature: Comparison Testing - DP830 - Inquire client tags and flags

As a client
I want to compare the responses from the IIB and Azure
So that I can see whether the responses are identical

Acceptance:
  (1) The responses from the IIB and Azure endpoints are identical
  (2) The status code are:
    * 83000 - Transaction Successful
    * 83000 - No current programme tags for the requested client
    * 83000 - No current flags for the requested client
    * 83001 - No matching client
    * 83002 - Invalid Client Number
    * 83009 - User not recognised


  @positive
  Scenario: Compare DP830 successful response when client has programme tags and client flags
    Given I create the correct api payload
    And   I send inquire participant request for client tags and flags to IIB endpoint
    And   I send inquire participant request for client tags and flags to Azure endpoint
    Then  I can see the responses are identical


  @positive
  Scenario Outline: Compare DP830 successful result
    Given I create the correct api payload for <client_type>
    And   I send inquire participant request for client tags and flags to IIB endpoint
    And   I send inquire participant request for client tags and flags to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | client_type               |
      | no_current_programme_tags |
      | no_current_flags          |


  @negative
  Scenario Outline: Compare DP830 responses when the client or user cannot be validated
    Given I create the api payload for <condition>
    And   I send inquire participant request for client tags and flags to IIB endpoint
    And   I send inquire participant request for client tags and flags to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | condition             |
      | no_matching_client    |
      | invalid_client_number |
      | missing_client_number |
      | user_not_recognised   |
