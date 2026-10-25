@IIB-AZURE-COMPARISON @SOAP-API @sc812-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - DP864 - Inquire hardship entitilement

  As a client
  I want to compare the responses from the IIB and Azure for DP864
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare DP864 successful response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
    | conditions      |
    | dental          |
    | food            |
    | hardship_count  |
    | advance_balance |
    | all |


  @negative
  Scenario Outline: Compare DP864 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions              |
      | client_not_recognised   |
      | transaction_unsuccessful|
