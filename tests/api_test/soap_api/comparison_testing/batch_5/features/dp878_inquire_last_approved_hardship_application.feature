@AZURE-REST-API @REST-API @dp878-comparison
Feature: Comparison Testing - DP878 - Inquire Last Approved Hardship Application

  As a client
  I want to send DP878 Inquire Last Approved Hardship Application requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes and messages are:
      * 87800 - Transaction Successful
      * 87801 - No matching record
      * 87811 - Client not recognised
    * A request that does not contain the minimum required data is expected to return a schema validation error

  Execution Note:
    * Missing clientNumber currently returns an Invalid Request response rather than the schema validation error described in the AC.
    * Missing transactionId is currently accepted and processed instead of returning a validation error.


  @positive @dp878-positive
  Scenario Outline: Compare DP878 successful responses between DataPower and Azure
    Given I create the DP878 api request for <condition>
    When I send DP878 request to DataPower endpoint
    And I send DP878 request to Azure endpoint
    Then I can see all the responses are identical for DP878

    Examples:
      | condition                              |
      | approved_hardship_application_found    |
      | no_approved_hardship_application_found |


  @negative @dp878-negative
  Scenario Outline: Compare DP878 unsuccessful responses between DataPower and Azure
    Given I create the DP878 api request for <condition>
    When I send DP878 request to DataPower endpoint
    And I send DP878 request to Azure endpoint
    Then I can see all the responses are identical for DP878

    Examples:
      | condition              |
      | missing_client_number  |
      | missing_transaction_id |
      | client_not_recognised  |
      | client_is_duplicate    |
