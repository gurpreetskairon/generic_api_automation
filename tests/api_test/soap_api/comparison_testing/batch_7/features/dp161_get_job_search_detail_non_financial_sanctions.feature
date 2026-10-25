@AZURE-REST-API @REST-API @dp161-comparison
Feature: Comparison Testing - DP161 - Get Job Search Detail for Non-Financial Sanctions

  As a client,
  I want to send DP161 Get Job Search Detail for Non-Financial Sanctions requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes are:
      * 16100 - Transaction Successful
      * 16101 - reportJobsearchID not found for this client
    * The expected HTTP response codes are:
      * 200 - Successful
      * 400 - reportJobsearchID not found for the client
      * 401 - Unauthorised
      * 404 - The requested resource was not found


  @positive @dp161-positive
  Scenario Outline: Compare DP161 successful response between DataPower and Azure
    Given I create the DP161 api payload for <condition>
    When I send DP161 request to DataPower endpoint
    And I send DP161 request to Azure endpoint
    Then I can see all the responses are identical for DP161

    Examples:
      | condition           |
      | successful_response |


  @negative @dp161-negative
  Scenario Outline: Compare DP161 unsuccessful responses between DataPower and Azure
    Given I create the DP161 api payload for <condition>
    When I send DP161 request to DataPower endpoint
    And I send DP161 request to Azure endpoint
    Then I can see all the responses are identical for DP161

    Examples:
      | condition                     |
      | missing_participant_id        |
      | invalid_client_number         |
      | report_jobsearch_id_not_found |
      | unauthorised                  |
      | resource_not_found            |

