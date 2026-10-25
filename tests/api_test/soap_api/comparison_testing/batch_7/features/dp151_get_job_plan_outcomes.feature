@AZURE-REST-API @REST-API @dp151-comparison
Feature: Comparison Testing - DP151 - Get Job Plan Outcomes

  As a client,
  I want to send DP151 Get Job Plan Outcomes requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected HTTP response codes are:
      * 200 - Successful Operation
      * 400 - Bad Request


  @positive @dp151-positive
  Scenario Outline: Compare DP151 successful responses between DataPower and Azure
    Given I create the DP151 api payload for <condition>
    When I send DP151 request to DataPower endpoint
    And I send DP151 request to Azure endpoint
    Then I can see all the responses are identical for DP151

    Examples:
      | condition                       |
      | successful_response             |
      | successful_empty_actions        |
      | successful_multiple_actions     |
      | successful_populated_activities |
      | successful_other_method         |
      | successful_null_end_date        |


  @negative @dp151-negative
  Scenario Outline: Compare DP151 bad request responses between DataPower and Azure
    Given I create the DP151 api payload for <condition>
    When I send DP151 request to DataPower endpoint
    And I send DP151 request to Azure endpoint
    Then I can see all the responses are identical for DP151

    Examples:
      | condition              |
      | missing_client_number  |
      | missing_transaction_id |
      | missing_source_system  |
