@AZURE-REST-API @REST-API @dp886-comparison
Feature: Comparison Testing - DP886 - Inquire Ongoing Applications Summary

  As a client
  I want to send DP886 inquire ongoing applications summary requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes and messages are:
      * 88600 - Transaction Successful
      * 88601 - No matching record
    * Missing mandatory field - Client number
    * Search period end earlier than search period start - Invalid Request

  @positive @dp886-positive
  Scenario Outline: Compare DP886 successful responses between DataPower and Azure
    Given I create the DP886 api request for <condition>
    When I send DP886 request to DataPower endpoint
    And I send DP886 request to Azure endpoint
    Then I can see all the responses are identical for DP886

    Examples:
      | condition                    |
      | ongoing_application_found    |
      | no_ongoing_application_found |


  @negative @dp886-negative
  Scenario Outline: Compare DP886 unsuccessful responses between DataPower and Azure
    Given I create the DP886 api request for <condition>
    When I send DP886 request to DataPower endpoint
    And I send DP886 request to Azure endpoint
    Then I can see all the responses are identical for DP886

    Examples:
      | condition                      |
      | missing_client_number          |
      | search_period_end_before_start |
