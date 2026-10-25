@SOAP-API @manageparticipant
Feature: Azure Integration - SC826 - Find Client

  As a client
  I want to verify the response from Azure match whats on file
  So that I can confirm SC826 is working as intended

  Acceptance:
  * Get a response from the Azure endpoint and verify it with whats on file

  Notes:
  #todo: jesse


  @positive
  Scenario Outline: Verify SC826 successful responses
    Given I create the correct api payload <payload_type>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses
    And   I can see subresult message <subresult_message> is the same in both responses
    And   I can see subresult code <subresult_code> is the same in both responses
    And   I can see the responses are identical for payload <payload_type>

    Examples:
      | payload_type | result_code | result_message         | subresult_code | subresult_message            |
      | all_but_ird  | 82600       | Transaction Successful | 00011          | Name search successful       |
      | dob_only     | 82600       | Transaction Successful | 00011          | Name search successful       |
      | full_name    | 82600       | Transaction Successful | 00011          | Name search successful       |
      | ird_only     | 82600       | Transaction Successful | 00009          | IRD number search successful |
      | name_gender  | 82600       | Transaction Successful | 00011          | Name search successful       |


  #The below script requires a secured client


  @positive
  Scenario Outline: Verify SC826 responses with a secured client
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | payload_type | result_code | result_message         | conditions     |
      | all_but_ird  | 82603       | Transaction Successful | secured_client |
      | dob_only     | 82603       | Transaction Successful | secured_client |
      | full_name    | 82603       | Transaction Successful | secured_client |
      | ird_only     | 82603       | Transaction Successful | secured_client |
      | name_gender  | 82603       | Transaction Successful | secured_client |


  @negative
  Scenario Outline: Verify SC826 responses with invalid data
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | payload_type | result_code | result_message      | conditions     |
      | all_but_ird  | 82610       | Invalid request     | invalid_gender |
      | all_but_ird  | 82611       | Invalid name search | invalid_name   |
      | ird_only     | 82610       | Invalid request     | invalid_ird    |
      | full_name    | 82611       | Invalid name search | invalid_name   |
      | name_gender  | 82610       | Invalid request     | invalid_gender |


  @negative
  Scenario Outline: Verify SC826 responses with invalid user
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | payload_type | result_code | result_message      | conditions   |
      | all_but_ird  | 82609       | User not recognised | invalid_user |
      | dob_only     | 82609       | User not recognised | invalid_user |
      | ird_only     | 82609       | User not recognised | invalid_user |
      | full_name    | 82609       | User not recognised | invalid_user |
      | name_gender  | 82609       | User not recognised | invalid_user |


  #The below script requires the environment to have 51 or more clients that share the same
  #names, gender and date of birth


  @negative
  Scenario Outline: Verify SC826 responses with results containing more than 50 entries
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | payload_type | result_code | result_message         | conditions |
      | all_but_ird  | 82602       | Search limit exceeded. | 50+Clients |
      | full_name    | 82602       | Search limit exceeded. | 50+Clients |
      | name_gender  | 82602       | Search limit exceeded. | 50+Clients |
