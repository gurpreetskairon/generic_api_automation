@REST-API
Feature: Comparison Testing - SC162 - Manage Job Search Detail For Non-Financial Sanction

  As a client,
  I want to send SC162 Manage Job Search Detail requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes and messages are:
      * 16200 - The post request was successful
      * 16201 - The data request is invalid


  @positive
  Scenario Outline: Compare SC162 successful transaction response
    Given I create the correct SC162 api request with different <conditions>
    And I send the SC162 request to IIB endpoint
    And I send the SC162 request to Azure endpoint
    Then I can see all the responses are identical for SC162

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC162 invalid request response
    Given I create the correct SC162 api request with different <conditions>
    And I send the SC162 request to IIB endpoint
    And I send the SC162 request to Azure endpoint
    Then I can see all the responses are identical for SC162

    Examples:
      | conditions      |
      | report_job_search_not_found |
