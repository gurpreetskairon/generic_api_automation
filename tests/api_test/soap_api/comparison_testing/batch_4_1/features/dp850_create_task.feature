@SOAP-API
Feature: Comparison Testing - DP850 - Create Task

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the DP850 responses are identical


  @positive
  Scenario Outline: Compare DP850 successful transaction response
    Given I create the correct DP850 api payload with different <conditions>
    And   I send the DP850 request to IIB endpoint
    And   I send the DP850 request to Azure endpoint
    Then  I can see all the responses are identical for DP850

    Examples:
      | conditions         |
      | successful_request |
