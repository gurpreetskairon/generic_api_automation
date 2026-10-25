@SOAP-API
Feature: Azure Integration - SC247 - Store client verification event

  As a client
  I want to verify the SC247 responses from Azure
  So that I can see whether the expected responses are returned


  @positive
  Scenario Outline: Verify SC247 successful responses
    Given I create the correct api payload
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | result_code | result_message         |
      | 24700       | Transaction Successful |


  @positive
  Scenario Outline: Verify SC247 responses for no matching clients
    Given I create the correct api payload with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses
    And   I can see subresult code <subresult_code> is the same in both responses
    And   I can see subresult message <subresult_msg> is the same in both responses

    Examples:
      | result_code | result_message           | subresult_code | subresult_msg      | conditions         |
      | 24710       | Transaction Unsuccessful | 1              | No matching client | no_matching_client |


  @negative
  Scenario Outline: Verify SC247 responses with invalid data
    Given I create the correct api payload with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses
    And   I can see subresult code <subresult_code> is the same in both responses
    And   I can see subresult message <subresult_msg> is the same in both responses

    Examples:
      | result_code | result_message  | subresult_code | subresult_msg                                | conditions                 |
      | 24701       | Invalid request | 5              | Invalid requestDateTime                      | invalid_datetime           |
      | 24701       | Invalid request | 2              | Invalid sourceSystem                         | invalid_sourcesystem       |
      | 24701       | Invalid request | 3              | Invalid transactionID                        | invalid_transactionid      |
      | 24701       | Invalid request | 4              | Invalid securityToken                        | invalid_securitytoken      |
      | 24701       | Invalid request | 16             | Invalid system                               | invalid_system             |
      | 24701       | Invalid request | 11             | Invalid documentTypeCode                     | invalid_documenttypecode   |
      | 24701       | Invalid request | 12             | Invalid dateOfBirthStatus                    | invalid_dateOfBirthStatus  |
      | 24701       | Invalid request | 13             | Invalid firstNameStatus                      | invalid_firstNameStatus    |
      | 24701       | Invalid request | 14             | Invalid familyNameStatus                     | invalid_familyNameStatus   |
      | 24701       | Invalid request | 15             | Invalid documentPhotoFacialRecognitionStatus | invalid_docStatus          |
      | 24701       | Invalid request | 17             | Invalid livenessPassStatus                   | invalid_livenesspassstatus |


  @negative
  Scenario Outline: Verify SC247 responses with an invalid client number
    Given I create the correct api payload with different <conditions>
    And   I send the request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | result_code | result_message        | conditions            |
      | 24702       | Invalid client number | invalid_client_number |
