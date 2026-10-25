@AZURE-SOAP-API @SOAP-API @sc898-integration @inquireparticipant
@inquireeligibility
Feature: Azure Integration - SC898 - Inquire Eligibility

  As a consumer of the SC898 SOAP service
  I want to validate successful and unsuccessful inquire eligibility responses
  So that the Azure integration behaves according to the WSDL and acceptance criteria

  Acceptance:
  * 89800 - Transaction Successful
  * 89801 - No Matching Client
  * 89802 - Invalid Client Number
  * 89803 - Client Number Is Missing
  * 89809 - User not recognised
  * Successful Click to Enrol eligibility response can include the following details:
    (1) flag code
    (2) flag description
    (3) status
    (4) expiry date

  Execution notes:
  * SC898 retrieves client flag status details for MyMSD Click to Enrol eligibility.
  * Click to Enrol eligibility is validated for active and expired C2E flag conditions.
  * The missing client number scenario returns an exception response with code 89803.
  * The no_c2e_flag scenario is excluded from automation because expiryDate behaviour is data-dependent and not part of the current acceptance criteria.


  @positive @successful_response
  Scenario: Check SC898 inquireEligibilityResponse schema
    Given I created the correct SC898 api payload
    And   I sent the inquire eligibility request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the request auditId, requestDateTime and transactionId returned in SOAP response header
    And   I can see the clientNumber and result code 89800 returned in the response SOAP header serviceResult


  @positive @result_code_89800 @successful_response @click_to_enrol
  Scenario Outline: Check SC898 successful Click to Enrol eligibility details
    Given I created the correct SC898 api payload for <client_flag_condition>
    And   I sent the inquire eligibility request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the result code 89800 returned in the response SOAP header serviceResult
    And   I can see Click to Enrol flag code "<flag_code>" returned
    And   I can see Click to Enrol flag description "<flag_description>" returned
    And   I can see Click to Enrol status "<status>" returned


    Examples:
      | client_flag_condition | flag_code | flag_description | status |
      | active_c2e_flag       | CLK2ENL   | Click To Enrol   | true   |
      | expired_c2e_flag      | CLK2ENL   | Click To Enrol   | false  |


  @negative
  Scenario Outline: Check SC898 negative business result code and message
    Given I created the SC898 api payload for <negative_condition>
    And   I sent the inquire eligibility request to the Azure endpoint
    Then  I can see result code <result_code> returned
    And   I can see result message "<result_message>" returned

    Examples:
      | negative_condition    | result_code | result_message        |
      | no_matching_client    | 89801       | No Matching Client    |
      | invalid_client_number | 89802       | Invalid Client Number |
      | user_not_recognised   | 89809       | User not recognised   |


  @negative @missing_client_number @exception_response
  Scenario: Check SC898 response when client number is missing
    Given I created the SC898 api payload for missing_client_number
    And   I sent the inquire eligibility request to the Azure endpoint
    Then  I can see exception code 89803 returned
    And   I can see exception message "Client Number Is Missing" returned
