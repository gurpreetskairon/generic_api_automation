@SOAP-API @inquireparticipant
Feature: Azure Integration - SC246 - Inquire Client Identity Verification Status

  As a client
  I want to verify the responses from the Azure
  So that I can see whether the responses are we expected

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Verify SC246 successful response
    Given I create the correct api payload
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses
    And   I can see the responses are identical

    Examples:
      | result_code | result_message         |
      | 24600       | Transaction Successful |


  @positive
  Scenario Outline: Verify SC246 responses for client with no id verification
    Given I create the correct api payload with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses
    And   I can see the responses are identical

    Examples:
      | result_code | result_message         | conditions               |
      | 24600       | Transaction Successful | no_identity_verification |


  @negative
  Scenario Outline: Verify SC246 responses with invalid data
    Given I create the correct api payload with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | result_code | result_message        | conditions            |
      | 24602       | No matching client    | no_matching_client    |
      | 24603       | Invalid client number | invalid_client_number |
      | 24604       | User not recognised   | user_not_recognised   |


  @negative
  Scenario Outline: Verify SC246 responses with invalid header values
    Given I create the correct api payload with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | result_code | result_message  | conditions            |
      | 24601       | Invalid request | invalid_sourcesystem  |
      | 24601       | Invalid request | invalid_transactionid |
      | 24601       | Invalid request | invalid_securitytoken |
