@AZURE-SOAP-API @SOAP-API @sc893-comparison
Feature: Comparison Testing - SC893 - Submit Temporary Additional Support Application

  As a client
  I want to send SC893 temporary additional support application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 89300 - Transaction Successful
      * 89301 - Transaction Unsuccessful
      * 89310 - Invalid Request

  Execution Note:
    * The 89301 - Transaction Unsuccessful scenario is not currently automated because
      there are no Splunk logs available to reliably determine or reproduce the condition
      where the application has not been recorded.


  @positive @sc893-positive
  Scenario Outline: Compare SC893 successful responses between IIB and Azure
    Given I create the SC893 api payload for <condition>
    When  I send SC893 request to IIB endpoint
    And   I send SC893 request to Azure endpoint
    Then  I can see all the responses are identical for SC893

    Examples:
      | condition           |
      | successful_response |


  @negative @sc893-negative
  Scenario Outline: Compare SC893 unsuccessful responses between IIB and Azure
    Given I create the SC893 api payload for <condition>
    When  I send SC893 request to IIB endpoint
    And   I send SC893 request to Azure endpoint
    Then  I can see all the responses are identical for SC893

    Examples:
      | condition       |
      | invalid_request |
