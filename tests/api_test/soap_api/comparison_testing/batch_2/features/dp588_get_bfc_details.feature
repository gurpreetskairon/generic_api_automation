@REST-API
Feature: Comparison Testing - DP588 - Get BFC Details

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the DP588 responses are identical


  @positive
  Scenario Outline: Compare DP588 successful transaction responses
    Given I create the correct DP588 api payload with different <conditions>
    And   I send the DP588 request to IIB endpoint
    And   I send the DP588 request to Azure endpoint
    Then  I can see all the responses are identical for DP588

    Examples:
      | conditions                   |
      | successful                   |
      | client_not_present           |



