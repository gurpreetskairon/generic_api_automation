@COMPARISON-REST-API
@REST-API
@dp871-comparison
Feature: Comparison Testing - DP871 - Manage Client Contact Details


  @positive
  Scenario Outline: Compare DP871 successful transaction response
    Given I create the DP871 comparison payload for "<condition>"
    When  I send the DP871 request to Azure endpoint
    And   I send the DP871 request to IIB endpoint
    Then  I can see all the responses are identical for DP871


    Examples:
      | condition                        |
      | update_communication_method_only |


  @negative
  Scenario Outline: Compare DP871 unsuccessful transaction response
    Given I create the DP871 comparison payload for "<condition>"
    When  I send the DP871 request to IIB endpoint
    And   I send the DP871 request to Azure endpoint
    Then  I can see all the responses are identical for DP871

    Examples:
      | condition                 |
      | invalid_request           |
      | client_not_recognised     |
      | duplicate_or_fraud_client |
      | duplicate_contact_type    |
      | incomplete_client_record  |
