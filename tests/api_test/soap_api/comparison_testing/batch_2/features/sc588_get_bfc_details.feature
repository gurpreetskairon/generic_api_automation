@REST-API
Feature: Comparison Testing - SC588 - Get BFC details

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC588 responses are identical


  @positive
  Scenario Outline: Compare SC588 successful transaction responses
    Given I create the correct SC588 api payload with different <conditions>
    And   I send the SC588 request to IIB endpoint
    And   I send the SC588 request to Azure endpoint
    Then  I can see all the responses are identical for SC588

    Examples:
      | conditions         |
      | successful         |
      | client_not_present |


