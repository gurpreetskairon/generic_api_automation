@AZURE-SOAP-API @SOAP-API @sc559-comparison
Feature: Comparison Testing - SC559 - Notify Expired Payments

  As a client
  I want to send SC559 notify expired payment requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 50000 - Transaction Successful - The payment has been successfully updated with the amount spent at expiry
      * 50024 - The request has failed the XML validation
      * 59999 - Technical failure

  Execution Note:
    * SC559 notifies the payment card service of expired payments and updates the payment with the amount spent at expiry.
    * Result code 59999 represents a technical failure and cannot be reliably triggered through automation.
    * The 59999 acceptance condition is therefore documented but is not included as a runnable comparison scenario.


  @positive @sc559-positive
  Scenario Outline: Compare SC559 successful responses between IIB and Azure
    Given I create the SC559 api payload for <condition>
    When  I send SC559 request to IIB endpoint
    And   I send SC559 request to Azure endpoint
    Then  I can see all the responses are identical for SC559

    Examples:
      | condition                  |
      | successful_expired_payment |


  @negative @sc559-negative
  Scenario Outline: Compare SC559 unsuccessful responses between IIB and Azure
    Given I create the SC559 api payload for <condition>
    When  I send SC559 request to IIB endpoint
    And   I send SC559 request to Azure endpoint
    Then  I can see all the responses are identical for SC559

    Examples:
      | condition   |
      | invalid_xml |
