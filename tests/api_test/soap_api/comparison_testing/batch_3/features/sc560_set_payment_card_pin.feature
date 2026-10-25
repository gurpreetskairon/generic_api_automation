@IIB-AZURE-COMPARISON @SOAP-API @sc560-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC560 - Inquire ongoing assistance

  As a client
  I want to compare the responses from the IIB and Azure for SC560
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare SC560 successful response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions             |
      | transaction_successful |


  @negative
  Scenario Outline: Compare SC560 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions          |
      | card_not_recognised |
