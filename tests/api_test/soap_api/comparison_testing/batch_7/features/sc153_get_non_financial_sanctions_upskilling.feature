@AZURE-REST-API @REST-API @sc153-comparison
Feature: Comparison Testing - SC153 - Get Non-Financial Sanctions Upskilling

  As a client,
  I want to send SC153 Get Non-Financial Sanctions Upskilling requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected HTTP result codes and messages are:
      * 200 - The get request was successful
      * 200 - Upskilling not found for this client
      * 400 - The data request is invalid. Check the error message for further information and resend the request with the corrected data
      * 401 - Unauthorised
      * 404 - The requested resource was not found


  @positive @sc153-positive
  Scenario Outline: Compare SC153 successful responses between IIB and Azure
    Given I create the SC153 api payload for <condition>
    When I send SC153 request to IIB endpoint
    And I send SC153 request to Azure endpoint
    Then I can see all the responses are identical for SC153

    Examples:
      | condition                    |
      | successful_response          |
      | no_upskilling_details        |


  @negative @sc153-negative
  Scenario Outline: Compare SC153 unsuccessful responses between IIB and Azure
    Given I create the SC153 api payload for <condition>
    When I send SC153 request to IIB endpoint
    And I send SC153 request to Azure endpoint
    Then I can see all the responses are identical for SC153

    Examples:
      | condition          |
      | invalid_request    |
      | unauthorised       |
      | resource_not_found |
