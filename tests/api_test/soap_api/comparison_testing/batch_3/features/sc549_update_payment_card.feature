@AZURE-SOAP-API @SOAP-API @sc549-comparison
Feature: Comparison Testing - SC549 - Update Payment Card

  As a client
  I want to send SC549 update payment card requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 50000 - Transaction Successful
      * 50001 - The payment card number is invalid
      * 50006 - The card in the request is blocked and cannot be allocated
      * 50007 - The card in the request is already in use by another client
      * 50009 - The card is already cancelled, no further update can be done
      * 50019 - The card in the request has active payments where balance is greater than 0
      * 50022 - The card cannot be maintained as the expiry date has been reached
      * 50024 - The request has failed the XML validation
      * 50034 - No further card allocations can be made as the limit has been reached
      * 50037 - At least one of Signature Required or Pin Required must be set to True
      * 50043 - The blocked reason of the payment card is unknown or invalid
      * 50044 - The card has a blocked status but no blocked reason has been provided
      * 59998 - The payment card is already being updated by another user. Please retry the action again

  Execution Note:
    * Result code 50034 requires a client that has reached the allowable payment card allocation limit.
      This scenario will be automated where suitable D11 test data is available.
    * Result code 59998 requires the payment card to already be in use by another user or to be out
      of sync between the Gateway and the external card provider system.
    * The 59998 scenario cannot be reliably reproduced through automation and is therefore not included
      as a runnable comparison scenario at this stage.


  @positive @sc549-positive
  Scenario Outline: Compare SC549 successful responses between IIB and Azure
    Given I create the SC549 api payload for <condition>
    When  I send SC549 request to IIB endpoint
    And   I send SC549 request to Azure endpoint
    Then  I can see all the responses are identical for SC549

    Examples:
      | condition                      |
      | successful_payment_card_update |


  @negative @sc549-negative
  Scenario Outline: Compare SC549 unsuccessful responses between IIB and Azure
    Given I create the SC549 api payload for <condition>
    When  I send SC549 request to IIB endpoint
    And   I send SC549 request to Azure endpoint
    Then  I can see all the responses are identical for SC549

    Examples:
      | condition                        |
      | invalid_card_number              |
      | blocked_card                     |
      | card_allocated_to_another_client |
#      | cancelled_card                    |
#      | card_with_active_payments         |
#      | expired_card                      |
      | invalid_xml                       |
      | card_allocation_limit_reached     |
      | pin_and_signature_not_required    |
      | invalid_block_reason              |
      | blocked_card_without_block_reason |
