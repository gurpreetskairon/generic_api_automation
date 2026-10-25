@AZURE-SOAP-API @SOAP-API @sc825-integration
@inquireparticipant
Feature: Azure Integration - SC825 - Inquire participant

  As a consumer of the SC825 SOAP service
  I want to validate successful and unsuccessful inquiry responses
  So that the integration behaves according to the WSDL and security requirements

  Acceptance:
  * 82500 - Transaction Successful
  * 82500 - Client is not secured
  * 82500 - Client is secured – requesting user has global access
  * 82500 - Client is secured – requesting user has temporary access to this client
  * 82501 - No matching record
  * 82502 - Transaction Successful - Requesting user does not have access to this secured client
  * 82509 - User not recognised

  Execution notes:
  * The temporary_access scenario is not executed in Azure integration testing because temporary access is time-bound and must be granted on the day of execution.
  * Keeping temporary_access enabled in regular Azure integration runs can cause false failures if the access has expired or has not been granted for the execution date.
  * The temporary_access scenario is retained in Azure-vs-IIB comparison testing, where the test data can be confirmed before execution.
  * Invalid token scenarios cover missing Security information and invalid credentials.
  * Invalid token scenarios are currently skipped in Azure integration testing.


  @positive
  @API-2912 @AC1 @positive @successful_response
  Scenario: Check SC825 inquireParticipantResponse schema
    Given I created the correct api payload
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the request auditId, requestDateTime and transactionId returned in SOAP response header
    And   I can see the clientNumber and result code 82500 returned in the response SOAP header serviceResult


  @positive
  Scenario Outline: Check SC825 successful transaction subresult details
    Given I created the correct api payload for <client_type>
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see the Transaction Successful returned
    And   I can see the result code 82500 returned in the response SOAP header serviceResult
    And   I can see subresult code <subresult_code> returned
    And   I can see subresult message "<subresult_message>" returned

    Examples:
      | client_type   | subresult_code | subresult_message                                     |
      | not_secured   | 1              | Client is not secured                                 |
      | global_access | 2              | Client is secured – requesting user has global access |


  @negative
  Scenario Outline: Check SC825 negative business result code and message
    Given I created the api payload for <negative_condition>
    And   I sent the inquire participant request to the Azure endpoint
    Then  I can see result code <result_code> returned
    And   I can see result message "<result_message>" returned

    Examples:
      | negative_condition | result_code | result_message                                                                       |
      | no_matching_client | 82501       | No matching record                                                                   |
      | no_client_access   | 82502       | Transaction Successful - Requesting user does not have access to this secured client |
      | user_not_found     | 82509       | User not recognised                                                                  |


  @negative @skip
  Scenario Outline: Check SC825 LDAP exception response
    Given I created the api payload with an invalid <token>
    And   I sent the exceptional inquire participant request to the Azure endpoint
    Then  I can see inquireParticipantException response schema returned
    And   I can see LDAP exception code <exception_code> returned

    Examples:
      | token                   | exception_code |
      | no Security information | 2717           |
      | invalid credentials     | 2702           |
