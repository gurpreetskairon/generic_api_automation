@AZURE-REST-API @REST-API @sc161-comparison
Feature: Comparison Testing - SC161 - Get Job Search Detail for Non-Financial Sanction

  As a client,
  I want to send SC161 Get Job Search Detail for Non-Financial Sanction requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected HTTP response codes and messages are:
      * 200 - The get request was successful
      * 400 - The data request is invalid. Check the error message for further information and resend the request with the corrected data
      * 401 - Unauthorised
      * 404 - The requested resource was not found


  @positive @sc161-positive
  Scenario Outline: Compare SC161 successful responses between IIB and Azure
    Given I create the SC161 api payload for <condition>
    When I send SC161 request to IIB endpoint
    And I send SC161 request to Azure endpoint
    Then I can see all the responses are identical for SC161

    Examples:
      | condition           |
      | successful_response |


  @negative @sc161-negative
  Scenario Outline: Compare SC161 unsuccessful responses between IIB and Azure
    Given I create the SC161 api payload for <condition>
    When I send SC161 request to IIB endpoint
    And I send SC161 request to Azure endpoint
    Then I can see all the responses are identical for SC161

    Examples:
      | condition                     |
      | missing_participant_id        |
      | invalid_client_number         |
      | report_jobsearch_id_not_found |
      | unauthorised                  |
      | resource_not_found            |
