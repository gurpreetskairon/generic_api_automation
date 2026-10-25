@REST-API
Feature: Comparison Testing - DP868 - Submit Hardship Application

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the DP868 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare DP868 successful transaction response
    Given I create the correct DP868 api payload with different <conditions>
    And   I send the DP868 request to IIB endpoint
    And   I send the DP868 request to Azure endpoint
    Then  I can see all the responses are identical for DP868

    Examples:
      | conditions             |
      | successful_transaction |
