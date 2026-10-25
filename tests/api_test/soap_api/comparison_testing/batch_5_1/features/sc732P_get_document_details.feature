@AZURE-SOAP-API @SOAP-API @sc732-comparison

Feature: Comparison Testing - SC732 - Get Document Details

  As a client,
  I want to send SC732 Get Document Details requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 71000 - Transaction successful
      * 71020 - Missing mandatory element: <value missing>
      * 71070 - Document identifier not recognised
      * 79999 - Unexpected system error - general exception returned with error print stack

  Execution Note:
    * Result code 79999 represents an integration infrastructure/system error and is documented in Acceptance but is not included as a runnable comparison scenario unless a reliable way to reproduce it is confirmed.


  @positive
  @sc732-positive
  Scenario Outline: Compare SC732 successful responses between IIB and Azure
    Given I create the SC732 api payload for <condition>
    When I send SC732 request to IIB endpoint
    And I send SC732 request to Azure endpoint
    Then I can see all the responses are identical for SC732

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc732-negative
  Scenario Outline: Compare SC732 unsuccessful responses between IIB and Azure
    Given I create the SC732 api payload for <condition>
    When I send SC732 request to IIB endpoint
    And I send SC732 request to Azure endpoint
    Then I can see all the responses are identical for SC732

    Examples:
      | condition                          |
      | missing_mandatory_data             |
      | document_identifier_not_recognised |
