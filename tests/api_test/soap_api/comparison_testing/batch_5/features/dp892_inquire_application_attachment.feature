@AZURE-REST-API @REST-API @dp892-comparison
Feature: Comparison Testing - DP892 - Inquire Application Attachment

  As a client
  I want to send DP892 Inquire Application Attachment requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes and messages are:
      * 89200 - Transaction Successful
      * 89201 - No Matching Record
    * Invalid request - A schema validation error has occurred while parsing the XML document


  @positive @dp892-positive
  Scenario Outline: Compare DP892 successful responses between DataPower and Azure
    Given I create the DP892 api request for <condition>
    When I send DP892 request to DataPower endpoint
    And I send DP892 request to Azure endpoint
    Then I can see all the responses are identical for DP892

    Examples:
      | condition                         |
      | application_attachment_retrieved  |


  @negative @dp892-negative
  Scenario Outline: Compare DP892 unsuccessful responses between DataPower and Azure
    Given I create the DP892 api request for <condition>
    When I send DP892 request to DataPower endpoint
    And I send DP892 request to Azure endpoint
    Then I can see all the responses are identical for DP892

    Examples:
    | condition                              |
    | invalid_request_missing_client_number  |
    | invalid_request_missing_case_reference |
    | no_application_or_attachment_found     |
