@AZURE-SOAP-API @SOAP-API @sc828-integration @manageparticipant
@inquireparticipant
Feature: Azure Integration - SC828 - Inquire participant

  As a consumer of the SC828 SOAP service
  I want to validate successful and unsuccessful inquiry responses based on client name and date of birth
  So that the integration behaves according to the WSDL and SC828 business matching rules

  Acceptance:
  * 82800 - Transaction Successful
  * 82801 - No matching record
  * 82810 - Invalid Request
  * Successful matched client response can include the following details:
    (1) client number
    (2) first name
    (3) family name
    (4) middle names
    (5) date of birth
    (6) gender
    (7) name confidence level
    (8) date of birth confidence level
    (9) client exists in SWIFTT

  * Successful matched client responses are compared for the following supported special client record types:
    (1) deceased client
    (2) fraud client

  Execution notes:
  * SC828 matching is based on client name and date of birth.
  * The expected business conditions and behaviour for locked/duplicate client matching are not confirmed.
  * As agreed with BA, locked/duplicate client behaviour should be covered during functional regression testing.


  @positive @AC1 @successful_response @result_code_82800 @response_schema
  Scenario: Check SC828 inquireParticipantResponse schema for successful transaction
    Given I created the correct SC828 api payload
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the response messageType returned as RESPONSE
    And   I can see the result code 82800 returned in the response SOAP header serviceResult
    And   I can see the result message "Transaction Successful" returned in the response SOAP header serviceResult
    And   I can see the detail of the matched client returned in the response


  @positive @AC1 @successful_response @matched_client_details @match_confidence @result_code_82800
  Scenario Outline: Check SC828 successful transaction matched client details
    Given I created the correct SC828 api payload for <client_match_condition>
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the result code 82800 returned in the response SOAP header serviceResult
    And   I can see the detail of the matched client returned in the response
    And   I can see client number, first name, family name, middle names, date of birth and gender returned in the response
    And   I can see nameConfidenceLevel <name_confidence_level> returned in the response
    And   I can see dateOfBirthConfidenceLevel <date_of_birth_confidence_level> returned in the response
    And   I can see clientExistsInSWIFTT returned in the response

    Examples:
      | client_match_condition       | name_confidence_level | date_of_birth_confidence_level |
      | full_name_100_dob_100        | 100                   | 100                            |
      | full_name_95_dob_100         | 95                    | 100                            |
      | full_name_85_dob_100         | 85                    | 100                            |
      | full_name_100_dob_day_month  | 100                   | day month                      |
      | full_name_100_dob_day_year   | 100                   | day year                       |
      | full_name_100_dob_month_year | 100                   | month year                     |


  @positive @AC1 @successful_response @special_client_records @result_code_82800
  Scenario Outline: Check SC828 returns matched client details for supported special client record types
    Given I created the correct SC828 api payload for <client_match_condition>
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the result code 82800 returned in the response SOAP header serviceResult
    And   I can see the result message "Transaction Successful" returned in the response SOAP header serviceResult
    And   I can see matched client details returned in the response
    And   I can see client number, first name, family name, middle names, date of birth and gender returned in the response
    And   I can see nameConfidenceLevel 100 returned in the response
    And   I can see dateOfBirthConfidenceLevel 100 returned in the response
    And   I can see clientExistsInSWIFTT returned in the response

    Examples:
      | client_match_condition |
      | deceased_client        |
      | fraud_client           |


  @positive @AC2 @no_matching_record @result_code_82801
  Scenario: Check SC828 no matching record result code and message
    Given I created the correct SC828 api payload for no_matching_client
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see result code 82801 returned
    And   I can see result message "No matching record" returned


  @negative @AC3 @invalid_request @too_short_name @result_code_82810
  Scenario: Check SC828 invalid request for too short client name
    Given I created the invalid SC828 api payload for too_short_name
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see result code 82810 returned
    And   I can see result message "Invalid Request" returned


  @negative @AC4 @invalid_request @missing_dob @result_code_82810
  Scenario: Check SC828 invalid request when date of birth is missing from request
    Given I created the invalid SC828 api payload for missing_dob
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see result code 82810 returned
    And   I can see result message "Invalid Request" returned
