@REST-API
Feature: Comparison Testing - SC1000 - Inquire Insights

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC1000 responses are identical


  @positive
  Scenario Outline: Compare SC1000 successful transaction responses
    Given I create the correct SC1000 api payload with different <conditions>
    And   I send the SC1000 request to IIB endpoint
    And   I send the SC1000 request to Azure endpoint
    Then  I can see all the responses are identical for SC1000

    Examples:
      | conditions              |
      | transaction_successful  |
