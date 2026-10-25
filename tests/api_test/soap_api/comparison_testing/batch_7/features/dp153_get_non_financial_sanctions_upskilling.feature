@AZURE-REST-API @REST-API @dp153-comparison
Feature: Comparison Testing - DP153 - Get Non-Financial Sanctions Upskilling

  As a client,
  I want to send DP153 Get Non-Financial Sanctions Upskilling requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes are:
      * 15300 - Transaction Successful
      * 15301 - Upskilling not found for this client
    * The expected HTTP response codes are:
      * 200 - Successful
      * 400 - Bad Request
      * 401 - Unauthorised
      * 404 - Not Found


  @positive @dp153-positive
  Scenario Outline: Compare DP153 successful response between DataPower and Azure
    Given I create the DP153 api payload for <condition>
    When I send DP153 request to DataPower endpoint
    And I send DP153 request to Azure endpoint
    Then I can see all the responses are identical for DP153

    Examples:
      | condition           |
      | successful_response |


  @negative @dp153-negative
  Scenario Outline: Compare DP153 unsuccessful responses between DataPower and Azure
    Given I create the DP153 api payload for <condition>
    When I send DP153 request to DataPower endpoint
    And I send DP153 request to Azure endpoint
    Then I can see all the responses are identical for DP153

    Examples:
      | condition                    |
      | bad_request                  |
      | unauthorised                 |
      | resource_not_found           |
      | upskilling_not_found         |
