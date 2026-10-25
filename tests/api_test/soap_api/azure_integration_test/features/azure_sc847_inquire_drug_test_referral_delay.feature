@AZURE-SOAP-API @SOAP-API @sc847-integration
@inquiredrugtestreferraldelay
Feature: Azure Integration - SC847 - Inquire Drug Test Referral Delay

  As a consumer of the SC847 SOAP service
  I want to validate successful and unsuccessful Drug Test Referral Delay responses
  So that the Azure integration behaves according to the WSDL and acceptance criteria

  Acceptance:
  * 84700 - Transaction Successful
  * 84701 - No matching record

  Notes:
    This service retrieves active Drug Test Referral Delay details for a requested client.
    If an active Drug Test Referral Delay is available for the client, the response will contain:
    * client number
    * category code
    * category description
    * type code
    * type description
    * notes, if available


  @positive @successful_response
  Scenario: Check SC847 inquireDrugTestReferralDelayResponse schema
    Given I created the correct SC847 api payload
    And   I sent the inquire drug test referral delay request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the request auditId and transactionId returned in SOAP response header
    And   I can see the clientNumber and result code 84700 returned in the response SOAP header serviceResult


  @positive @result_code_84700 @successful_response @drug_test_referral_delay
  Scenario Outline: Check SC847 successful Drug Test Referral Delay details
    Given I created the correct SC847 api payload for <dtrd_condition>
    And   I sent the inquire drug test referral delay request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the result code 84700 returned in the response SOAP header serviceResult
    And   I can see Drug Test Referral Delay category code "DRUGTESTREFERRALDELAY" returned
    And   I can see Drug Test Referral Delay category description "Drug Test - Referral Delay" returned
    And   I can see Drug Test Referral Delay type code "<type_code>" returned
    And   I can see Drug Test Referral Delay type description "<type_description>" returned
#And   I can see Drug Test Referral Delay effective start date returned

    Examples:
      | dtrd_condition                      | type_code                  | type_description                      |
      | dtrd_prescription_medication        | PRESCRIPTIONMEDICATION     | Drugs - Prescription medication       |
      | dtrd_receiving_treatment            | RECEIVINGTREATMENT         | Drugs - Receiving treatment           |
      | dtrd_awaiting_treatment             | AWAITINGTREATMENT          | Drugs - Awaiting treatment            |
      | dtrd_diagnosed_dependence           | DIAGNOSEDDEPENDENCE        | Drugs - Diagnosed dependence          |
      | dtrd_drug_help_required             | DRUGHELPREQUIRED           | Drugs - Client needs help to stop     |
      | dtrd_drug_other                     | DRUGOTHER                  | Drugs - Other                         |
      | dtrd_drug_no_good_sufficient_reason | DRUGNOGOODSUFFICIENTREASON | Drugs - No good and sufficient reason |
      | dtrd_drug_brief_interventions       | DRUGBRIEFINTERVENTIONS     | Drugs - Brief interventions           |
      | dtrd_drug_referred_assessment       | DRUGREFERREDASSESSMENT     | Drugs - Referred for assessment       |


  @positive @result_code_84701 @no_matching_record
  Scenario Outline: Check SC847 no matching record response when client has no active Drug Test Referral Delay
    Given I created the correct SC847 api payload for <dtrd_condition>
    And   I sent the inquire drug test referral delay request to the Azure endpoint
    Then  I can see the No matching record returned
    And   I can see the result code 84701 returned in the response SOAP header serviceResult
    And   I can see the clientNumber returned in the response SOAP header serviceResult

    Examples:
      | dtrd_condition |
      | no_active_dtrd |
