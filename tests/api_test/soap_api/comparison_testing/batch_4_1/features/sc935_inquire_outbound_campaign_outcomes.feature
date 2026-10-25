@REST-API
Feature: Comparison Testing - SC935 - Inquire Outbound Campaign Call Outcomes


  Scenario Outline: Compare SC935 successful transaction response
    Given I create the correct SC935 api request with different <conditions>
    And   I send the SC935 request to IIB endpoint
    And   I send the SC935 request to Azure endpoint
    Then  I can see all the responses are identical for SC935

    Examples:
      | conditions             |
      | successful_transaction |


  Scenario Outline: Compare SC935 unsuccessful transaction response
    Given I create the correct SC935 api request with different <conditions>
    And   I send the SC935 request to IIB endpoint
    And   I send the SC935 request to Azure endpoint
    Then  I can see all the responses are identical for SC935

    Examples:
      | conditions      |
      | invalid_request |
