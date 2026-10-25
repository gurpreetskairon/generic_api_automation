@AZURE-REST-API @REST-API @sc151-comparison
Feature: Comparison Testing - SC151 - Get Job Plan Outcomes

  As a client,
  I want to send SC151 Get Job Plan Outcomes requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected HTTP response codes and messages are:
      * 200 - The get request was successful
      * 400 - The data request is invalid. Check the error message for further information and resend the request with the corrected data
      * 500 - An internal server error occurred. Contact your administrator for more information
      * 500 - An unexpected error occurred. Check the error message for further information

  Execution Note:
    * Internal server error is not currently included as a runnable automation scenario as it cannot be reliably reproduced.
    * Unexpected error will be validated if a reproducible condition can be identified.


  @positive @sc151-positive
  Scenario Outline: Compare SC151 successful responses between IIB and Azure
    Given I create the SC151 api payload for <condition>
    When I send SC151 request to IIB endpoint
    And I send SC151 request to Azure endpoint
    Then I can see all the responses are identical for SC151

    Examples:
      | condition                       |
      | successful_response             |
      | successful_empty_actions        |
      | successful_multiple_actions     |
      | successful_populated_activities |
      | successful_other_method         |
      | successful_null_end_date        |


  @negative @sc151-negative
  Scenario Outline: Compare SC151 unsuccessful responses between IIB and Azure
    Given I create the SC151 api payload for <condition>
    When I send SC151 request to IIB endpoint
    And I send SC151 request to Azure endpoint
    Then I can see all the responses are identical for SC151

    Examples:
      | condition              |
      | missing_client_number  |
      | missing_transaction_id |
      | missing_source_system  |
