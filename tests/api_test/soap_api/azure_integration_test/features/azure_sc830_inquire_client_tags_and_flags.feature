@AZURE-SOAP-API @SOAP-API @sc830-integration
@inquireclienttagsandflags
@inquireparticipant
Feature: Azure Integration - SC830 - Inquire client tags and flags

  As a consumer of the SC830 SOAP service
  I want to validate successful and unsuccessful client tags and flags inquiry responses
  So that the integration behaves according to the SC830 acceptance criteria

  Acceptance:
  * 83000 - Transaction Successful
  * 83000 - No current programme tags for the requested client
  * 83000 - No current flags for the requested client
  * 83001 - No matching client
  * 83002 - Invalid Client Number
  * 83009 - User not recognised

  Notes:
    Programme tag and client flag reference codes are indicative and may change over time.
    This automation validates selected returned values only, not the full reference-code list.


  @positive
  @AC1 @result_code_83000 @successful_response @has_programme_tags_and_client_flags
  Scenario: Check SC830 successful transaction response with programme tags and client flags
    Given I created the correct api payload
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see result code 83000 returned
    And   I can see result message "Transaction Successful" returned
    And   I can see the request auditId, requestDateTime and transactionId returned in SOAP response header
    And   I can see the clientNumber returned in the response SOAP header serviceResult
    And   I can see programme tag details returned
    And   I can see client flag details returned


  @positive
  @AC1 @result_code_83000 @programme_tag_details
  Scenario Outline: Check SC830 programme tag category and tag details returned for the client
    Given I created the correct api payload for <client_type>
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see result code 83000 returned
    And   I can see result message "Transaction Successful" returned
    And   I can see programme tag category code "<category_code>" returned
    And   I can see programme tag category description "<category_description>" returned
    And   I can see programme tag code "<tag_code>" returned
    And   I can see programme tag description "<tag_description>" returned


    Examples:
      | client_type    | category_code | category_description                                       | tag_code | tag_description             |
      | has_tags_flags | CSMGMTAPPR    | Indicates the formal approach to case managing the client. | ISRP     | Integrated Service Response |


  @positive
  @AC1 @result_code_83000 @client_flag_details
  Scenario Outline: Check SC830 client flag details returned for the client
    Given I created the correct api payload for <client_type>
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see result code 83000 returned
    And   I can see result message "Transaction Successful" returned
    And   I can see client flag code "<flag_code>" returned
    And   I can see client flag description "<flag_description>" returned


    Examples:
      | client_type    | flag_code | flag_description      |
      | has_tags_flags | ENBCLKENL | Enable Click To Enrol |


  @positive
  @AC2 @result_code_83000 @no_current_programme_tags
  Scenario: Check SC830 response when the client has no current programme tags
    Given I created the correct api payload for no_current_programme_tags
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see result code 83000 returned
    And   I can see result message "Transaction Successful" returned
    And   I can see subresult code 1 returned
    And   I can see subresult message "No current programme tags for the requested client" returned


  @positive
  @AC3 @result_code_83000 @no_current_flags
  Scenario: Check SC830 response when the client has no current flags
    Given I created the correct api payload for no_current_flags
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see result code 83000 returned
    And   I can see result message "Transaction Successful" returned
    And   I can see subresult code 2 returned
    And   I can see subresult message "No current flags for the requested client" returned


  @positive
  @AC2 @AC3 @result_code_83000 @no_current_programme_tags_and_flags
  Scenario: Check SC830 response when the client has no current programme tags and no current flags
    Given I created the correct api payload for no_current_programme_tags_and_flags
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see result code 83000 returned
    And   I can see result message "Transaction Successful" returned
    And   I can see subresult code 1 and message "No current programme tags for the requested client" returned
    And   I can see subresult code 2 and message "No current flags for the requested client" returned


  @negative
  @AC4 @result_code_83001 @no_matching_client
  Scenario: Check SC830 response when the client does not exist in CMS
    Given I created the api payload for no_matching_client
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see result code 83001 returned
    And   I can see result message "No Matching Client" returned


  @negative
  @AC5 @result_code_83002 @invalid_client_number
  Scenario Outline: Check SC830 response when the client number is invalid or missing
    Given I created the api payload for <negative_condition>
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see result code 83002 returned
    And   I can see result message "Invalid Client Number" returned

    Examples:
      | negative_condition    |
      | invalid_client_number |
      | missing_client_number |


  @negative
  @AC6 @result_code_83009 @user_not_recognised
  Scenario: Check SC830 response when the user is not recognised
    Given I created the api payload for user_not_recognised
    And   I sent the inquire participant request for client tags and flags to the Azure endpoint
    Then  I can see result code 83009 returned
    And   I can see result message "User not recognised" returned
