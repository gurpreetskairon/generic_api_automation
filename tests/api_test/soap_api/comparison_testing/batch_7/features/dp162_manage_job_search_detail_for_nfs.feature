@AZURE-REST-API @REST-API @dp162-comparison
Feature: Comparison Testing - DP162 - Manage Job Search Detail For Non-Financial Sanction

  As a client,
  I want to send DP162 Manage Job Search Detail requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes are:
      * 16200 - Update successful
      * 16201 - Errors found
      * 90004 - Invalid Credentials


  @positive
  Scenario Outline: Compare DP162 successful response between DataPower and Azure
    Given I create the DP162 api payload for <condition>
    When I send DP162 request to DataPower endpoint
    And I send DP162 request to Azure endpoint
    Then I can see all the responses are identical for DP162

    Examples:
      | condition              |
      | successful_transaction |


  @negative
  Scenario Outline: Compare DP162 unsuccessful response between DataPower and Azure
    Given I create the DP162 api payload for <condition>
    When I send DP162 request to DataPower endpoint
    And I send DP162 request to Azure endpoint
    Then I can see all the responses are identical for DP162

    Examples:
      | condition       |
      | invalid_request |
      | unauthorised    |
