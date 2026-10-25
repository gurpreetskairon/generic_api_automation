@SOAP-API
Feature: Azure Integration - SC824 - Inquire provider user

  As a client
  I want to verify the responses from the Azure
  So that I can see whether the responses are we expected

  (1) The responses from the Azure endpoints are we expected
  (2) The user can get the following status:
      * 82400 - Transaction Successful
      * 82401 - Participant (i.e. client or provider user) is not recognised.
      * 82402 - Participant detail not available
      * 80099 - Result not recognized

Notes:
* This SC uses a providers, provider members external user account username found in cms
  -CMS Provider home page > Relationships > Provider Members > click name > administration


  @positive
  Scenario Outline: Verify SC824 successful response
    Given I create the correct api payload
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the result code <result_code> is the same in both responses
    And   I can see the result message <result_message> is the same in both responses
    And   I can see the email address in the response matches

    Examples:
      | result_code | result_message         |
      | 82400       | Transaction Successful |


  @positive
  Scenario Outline: Verify SC824 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the result code <result_code> is the same in both responses
    And   I can see the result message <result_message> is the same in both responses

    Examples:
      | conditions     | result_code | result_message            |
      | not_recognised | 82401       | Client is not recognised. |
#    | no_details    | 82402       |Participant detail not available| #CANNOT FIND/CREATE DATA


#  @positive
#  Scenario Outline: Verify SC825 successful result and subresult
#    Given I create the correct api payload for <client_type>
#    And   I send inquire participant request to IIB endpoint
#    And   I send inquire participant request to Azure endpoint
#    Then  I can see result code <result_code> is the same in both responses
#    And   I can see result message "<result_message>" is the same in both responses
#    And   I can see subresult code <subresult_code> is the same in both responses
#    And   I can see subresult message "<subresult_message>" is the same in both responses
#    Examples:
#      | client_type      | result_code | result_message         | subresult_code | subresult_message                                                      |
#      | not_secured      | 82500       | Transaction Successful | 1              | Client is not secured                                                  |
#      | global_access    | 82500       | Transaction Successful | 2              | Client is secured – requesting user has global access                  |
#      | temporary_access | 82500       | Transaction Successful | 3              | Client is secured – requesting user has temporary access to this client|
#
#
#  @negative
#  Scenario Outline: Verify SC825 responses when SOAPAction is missing or invalid
#    Given I create the api payload with different <conditions>
#    And   I send inquire participant request to IIB endpoint
#    And   I send the inquire participant request to Azure endpoint
#    Then  I can see the responses are identical
#
#    Examples:
#      | conditions                  |
#      | invalid SOAPAction          |
#      | missing SOAPAction          |
#
#   @negative @skip
#  Scenario Outline: Verify SC825 LDAP exception response when security details are missing or invalid
#    Given I create the api payload with different <conditions>
#    And   I send inquire participant request to IIB endpoint
#    And   I send the inquire participant request to Azure endpoint
#    Then  I can see inquireParticipantException response is returned in both responses
#    And   I can see LDAP exception code <exception_code> is returned in both responses
#
#  Examples:
#    | conditions             | exception_code |
#    | missing header         | 2717           |
#    | invalid credentials    | 2702           |
#    | missing security token | 2717           |
#
#      # Note: invalid security token currently returns 82509 / User not recognised,
#      # which is already covered by the user_not_found business validation scenario.
#      # Pending lead confirmation whether this needs separate coverage as its own input condition.
##    | invalid security token | 2702           |
#
#  @negative
#  Scenario Outline: Verify SC825 responses when the client or user cannot be validated
#    Given I create the api payload for <condition>
#    And   I send inquire participant request to IIB endpoint
#    And   I send inquire participant request to Azure endpoint
#    Then  I can see the responses are identical
#    Then  I can see result code <result_code> is the same in both responses
#    And   I can see result message "<result_message>" is the same in both responses
#
#    Examples:
#      | condition          | result_code | result_message                                                                       |
#      | no_matching_client | 82501       | No matching record                                                                   |
#      | no_client_access   | 82502       | Transaction Successful - Requesting user does not have access to this secured client |
#      | user_not_found     | 82509       | User not recognised                                                                  |
