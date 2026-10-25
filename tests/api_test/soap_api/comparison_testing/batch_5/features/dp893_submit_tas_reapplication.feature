@AZURE-REST-API @REST-API @dp893-comparison
Feature: Comparison Testing - DP893 - Submit TAS Reapplication

  As a client
  I want to send DP893 Submit TAS Reapplication requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result code and message are:
      * 89300 - Transaction Successful
    * Invalid request - A schema validation error has occurred while parsing the XML document


  @positive @dp893-positive
  Scenario Outline: Compare DP893 successful responses between DataPower and Azure
    Given I create the DP893 api request for <condition>
    When I send DP893 request to DataPower endpoint
    And I send DP893 request to Azure endpoint
    Then I can see all the responses are identical for DP893

    Examples:
      | condition                   |
      | tas_reapplication_submitted |


  @negative @dp893-negative
  Scenario Outline: Compare DP893 unsuccessful responses between DataPower and Azure
    Given I create the DP893 api request for <condition>
    When I send DP893 request to DataPower endpoint
    And I send DP893 request to Azure endpoint
    Then I can see all the responses are identical for DP893

    Examples:
      | condition                   |
      | invalid_request             |
      | invalid_client_info_changed |
