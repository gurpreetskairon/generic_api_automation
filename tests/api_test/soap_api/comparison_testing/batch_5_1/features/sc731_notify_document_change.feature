@AZURE-SOAP-API @SOAP-API @sc731-comparison

Feature: Comparison Testing - SC731 - Notify Document Change

  As a client,
  I want to send SC731 Notify Document Change requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 71000 - Transaction successful
      * 79999 - Unexpected system error - general exception returned with error printstack

  Execution Note:
    * Result code 79999 represents an integration infrastructure/system error and is documented in Acceptance but is not included as a runnable comparison scenario unless a reliable way to reproduce it is confirmed.
    * 71020 is included as additional runtime coverage for a missing scannedImageRef, based on observed IIB behaviour, although it is not currently documented in the SC731 acceptance criteria.

  @positive
  @sc731-positive
  Scenario Outline: Compare SC731 successful responses between IIB and Azure
    Given I create the SC731 api payload for <condition>
    When I send SC731 request to IIB endpoint
    And I send SC731 request to Azure endpoint
    Then I can see all the responses are identical for SC731

    Examples:
      | condition           |
      | successful_response |


   @negative
   @sc731-negative
   Scenario Outline: Compare SC731 validation responses between IIB and Azure
    Given I create the SC731 api payload for <condition>
    When I send SC731 request to IIB endpoint
    And I send SC731 request to Azure endpoint
    Then I can see all the responses are identical for SC731

    Examples:
      | condition                 |
      | missing_scanned_image_ref |
