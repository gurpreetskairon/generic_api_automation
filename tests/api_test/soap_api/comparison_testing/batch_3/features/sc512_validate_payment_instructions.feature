@AZURE-SOAP-API @SOAP-API @sc512-comparison
Feature: Comparison Testing - SC512 - Validate Payment Instructions

  As a client
  I want to send SC512 validate payment instruction requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 50000 - Transaction Successful
      * 50001 - The payment card number is invalid
      * 50002 - The payment expiry date exceeds the date the card expires
      * 50003 - The payment instruction cannot be added to the card as the card has reached its limit of active payments
      * 50004 - The payment instruction cannot be added to the card as the payment exceeds the card's total value limit
      * 50005 - The EFTPOS Gateway is currently unavailable
      * 50024 - The request has failed the XML validation
      * 50049 - Payment instructions cannot be added as the card is blocked or expired

  Execution Note:
    * Result code 50005 requires the EFTPOS Gateway to be unavailable and cannot be reliably triggered through automation.
    * The 50005 acceptance condition is therefore documented but is not included as a runnable comparison scenario.


  @positive @sc512-positive
  Scenario Outline: Compare SC512 successful responses between IIB and Azure
    Given I create the SC512 api payload for <condition>
    When  I send SC512 request to IIB endpoint
    And   I send SC512 request to Azure endpoint
    Then  I can see all the responses are identical for SC512

    Examples:
      | condition                     |
      | successful_payment_validation |


  @negative @sc512-negative
  Scenario Outline: Compare SC512 unsuccessful responses between IIB and Azure
    Given I create the SC512 api payload for <condition>
    When  I send SC512 request to IIB endpoint
    And   I send SC512 request to Azure endpoint
    Then  I can see all the responses are identical for SC512

    Examples:
      | condition                          |
      | invalid_card_number                |
      | payment_expiry_exceeds_card_expiry |
      | active_payment_limit_reached       |
      | card_total_value_limit_exceeded    |
      | invalid_xml                        |
      | blocked_or_expired_card            |
