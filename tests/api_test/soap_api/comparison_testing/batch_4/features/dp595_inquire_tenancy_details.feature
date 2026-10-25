@comparison
Feature: Comparison Testing - DP595 - Inquire Tenancy Details

  As a client
  I want to send DP595 Inquire Tenancy Details requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP595 successful responses between IIB and Azure
    Given I create the DP595 api payload for <condition>
    When  I send the DP595 request to IIB endpoint
    And   I send the DP595 request to Azure endpoint
    Then  I can see all the responses are identical for DP595

    Examples:
      | condition              |
      | transaction_successful |
