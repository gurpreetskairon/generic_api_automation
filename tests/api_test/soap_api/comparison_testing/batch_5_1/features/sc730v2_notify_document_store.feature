@AZURE-SOAP-API @SOAP-API @sc730v2-comparison

Feature: Comparison Testing - SC730V2 - Notify Document Store

  As a client,
  I want to send SC730V2 Notify Document Store requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 71000 - Transaction successful
      * 71010 - A document is already registered with this document reference id
      * 71020 - Missing mandatory element: <value missing>
      * 71030 - The <value> element contains invalid content
      * 71040 - User account does not exist / user account is disabled
      * 71070 - Document identifier not recognised
      * 79999 - Unexpected system error

  Execution Note:
    * SC730V2 is state-changing and successful scannedImageRef values cannot be reused.
    * Successful comparison generates separate unique scannedImageRef values for IIB and Azure.
    * 71030 and 71040 are documented but are not currently included as runnable scenarios until reliable input/test data is confirmed.
    * 79999 cannot be reliably reproduced through automation.


  @positive
  @sc730v2-positive
  Scenario Outline: Compare SC730V2 successful responses between IIB and Azure
    Given I create the SC730V2 api payload for <condition>
    When I send SC730V2 request to IIB endpoint
    And I send SC730V2 request to Azure endpoint
    Then I can see all the responses are identical for SC730V2

    Examples:
      | condition           |
      | successful_response |



  @negative
  @sc730v2-negative
  Scenario Outline: Compare SC730V2 document validation responses between IIB and Azure
    Given I create the SC730V2 api payload for <condition>
    When I send SC730V2 request to IIB endpoint
    And I send SC730V2 request to Azure endpoint
    Then I can see all the responses are identical for SC730V2

    Examples:
      | condition                          |
      | duplicate_document_reference       |


  @negative
  @sc730v2-negative
  Scenario Outline: Compare SC730V2 request validation responses between IIB and Azure
    Given I create the SC730V2 api payload for <condition>
    When I send SC730V2 request to IIB endpoint
    And I send SC730V2 request to Azure endpoint
    Then I can see all the responses are identical for SC730V2

    Examples:
      | condition              |
      | missing_mandatory_data |
      | invalid_request_data   |


 @negative
  @sc730v2-negative
  Scenario Outline: Compare SC730V2 security validation responses between IIB and Azure
    Given I create the SC730V2 api payload for <condition>
    When I send SC730V2 request to IIB endpoint
    And I send SC730V2 request to Azure endpoint
    Then I can see all the responses are identical for SC730V2

    Examples:
      | condition              |
      | invalid_security_token |
