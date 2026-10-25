@comparison
Feature: Comparison Testing - DP833 - Inquire Communication

  As a client
  I want to send DP833 inquire communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP833 successful responses between IIB and Azure
    Given I create the DP833 api payload for <condition>
    When  I send DP833 request to IIB endpoint
    And   I send DP833 request to Azure endpoint
    Then  I can see all the responses are identical for DP833

    Examples:
      | condition                    |
      | transaction_successful       |
      | no_current_notification      |
