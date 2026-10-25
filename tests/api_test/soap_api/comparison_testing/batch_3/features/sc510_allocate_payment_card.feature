@IIB-AZURE-COMPARISON @SOAP-API @sc510-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC510 - allocate payment card

  As a client
  I want to compare the responses from the IIB and Azure for SC510
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare SC510 successful response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions             |
      | transaction_successful |


  @negative
  Scenario Outline: Compare SC510 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions           |
      | invalid_payment_card |
      | card_already_in_use  |
      | schema_validation    |
      | card_limit_reached   |
      | blocked_card         |
