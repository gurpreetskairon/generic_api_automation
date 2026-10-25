@AZURE-SOAP-API @SOAP-API @sc547-comparison
Feature: Comparison Testing - SC547 - Update Payment

  As a client
  I want to send SC547 update payment requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 50000 - Transaction Successful
      * 50011 - The card number does not belong to an active card
      * 50012 - The card number is not recognised in the system
      * 50015 - The payment reference in the request is not recognised
      * 50016 - The payment has expired
      * 50024 - The request has failed the XML validation
      * 50027 - The amount of the payment cannot be updated
      * 50028 - The bank account the payment is to be withdrawn from cannot be updated
      * 50029 - The payment reference to be updated/transferred does not exist on the card number sent in the request
      * 50041 - The reconciliation reference for the payment cannot be updated
      * 59998 - The payment card is already being updated by another user. Please retry the action again

  Execution Note:
    * Result code 59998 requires the payment card to already be in use or out of sync between the Gateway
      and the external card provider system.
    * The 59998 scenario may only be reproducible through manual testing and is therefore not included
      as a runnable comparison scenario at this stage.


  @positive @sc547-positive
  Scenario Outline: Compare SC547 successful responses between IIB and Azure
    Given I create the SC547 api payload for <condition>
    When  I send SC547 request to IIB endpoint
    And   I send SC547 request to Azure endpoint
    Then  I can see all the responses are identical for SC547

    Examples:
      | condition                 |
      | successful_payment_update |


#  @negative @sc547-negative
#  Scenario Outline: Compare SC547 unsuccessful responses between IIB and Azure
#    Given I create the SC547 api payload for <condition>
#    When I send SC547 request to IIB endpoint
#    And I send SC547 request to Azure endpoint
#    Then I can see all the responses are identical for SC547
#
#    Examples:
#      | condition                             |
#      | inactive_card                         |
#      | unrecognised_card                     |
#      | unrecognised_source_payment_reference |
#      | expired_payment                       |
#      | invalid_xml                           |
#      | different_payment_amount              |
#      | different_debit_account_code          |
#      | payment_reference_not_on_card         |
#      | different_reconciliation_reference    |
