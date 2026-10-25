@COMPARISON-REST-API
@REST-API
@dp811-comparison
@circumstance
Feature: Comparison Testing - DP811 - Inquire Circumstance


  Scenario Outline: Compare DP811 successful transaction response
    Given I create the DP811 comparison request for "<condition>"
    And   I send the DP811 request to IIB endpoint
    And   I send the DP811 request to Azure endpoint
    Then  I can see all the responses are identical for DP811

    Examples:
      | condition          |
      | success            |
      | no_matching_record |


  Scenario Outline: Compare DP811 unsuccessful transaction response
    Given I create the DP811 comparison request for "<condition>"
    And   I send the DP811 request to IIB endpoint
    And   I send the DP811 request to Azure endpoint
    Then  I can see all the responses are identical for DP811

    Examples:
      | condition             |
      | invalid_request       |
      | client_not_recognised |
