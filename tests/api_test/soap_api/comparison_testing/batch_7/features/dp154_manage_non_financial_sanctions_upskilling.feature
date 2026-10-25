@AZURE-REST-API @REST-API @dp154-comparison
Feature: Comparison Testing - DP154 - Manage Non-Financial Sanctions Upskilling

  As a client,
  I want to send DP154 Manage Non-Financial Sanctions Upskilling requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes are:
      * 15400 - Upskilling data updated
    * The expected HTTP response codes are:
      * 200 - Successful
      * 400 - Bad Request
      * 401 - Unauthorised
      * 404 - Not Found


  @positive @dp154-positive
  Scenario Outline: Compare DP154 successful response between DataPower and Azure
    Given I create the DP154 api payload for <condition>
    When I send DP154 request to DataPower endpoint
    And I send DP154 request to Azure endpoint
    Then I can see all the responses are identical for DP154

    Examples:
      | condition           |
      | successful_response |


  @negative @dp154-negative
  Scenario Outline: Compare DP154 unsuccessful responses between DataPower and Azure
    Given I create the DP154 api payload for <condition>
    When I send DP154 request to DataPower endpoint
    And I send DP154 request to Azure endpoint
    Then I can see all the responses are identical for DP154

    Examples:
      | condition                     |
      | missing_client_number         |
      | missing_upskilling_id         |
      | invalid_upskilling_id_format  |
#      | unauthorised                  |
      | resource_not_found            |
