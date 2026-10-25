@AZURE-SOAP-API @SOAP-API @sc558-comparison
Feature: Comparison Testing - SC558 - Inquire Payment Details

  As a client
  I want to send SC558 payment detail requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 50000 - Transaction Successful - The payment details have been returned successfully
      * 50015 - The payment reference in the request is not recognised
      * 50024 - The request has failed the XML validation
      * 59999 - Technical failure

  Execution Note:
    * SC558 retrieves the current balance and transaction history for an active or reconciled
      payment instruction recognised by the provider system.
    * The service validates the payment instruction reference and fails on the first error encountered.
    * Result code 59999 represents a technical failure and cannot be reliably triggered through automation.
    * The 59999 acceptance condition is therefore documented but is not included as a runnable
      comparison scenario at this stage.


  @positive @sc558-positive
  Scenario Outline: Compare SC558 successful responses between IIB and Azure
    Given I create the SC558 api payload for <condition>
    When  I send SC558 request to IIB endpoint
    And   I send SC558 request to Azure endpoint
    Then  I can see all the responses are identical for SC558

    Examples:
      | condition                  |
      | successful_payment_details |


  @negative @sc558-negative
  Scenario Outline: Compare SC558 unsuccessful responses between IIB and Azure
    Given I create the SC558 api payload for <condition>
    When  I send SC558 request to IIB endpoint
    And   I send SC558 request to Azure endpoint
    Then  I can see all the responses are identical for SC558

    Examples:
      | condition                      |
      | unrecognised_payment_reference |
      | invalid_xml                    |
