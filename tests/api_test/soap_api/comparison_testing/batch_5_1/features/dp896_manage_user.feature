@comparison
Feature: Comparison Testing - DP896 - Manage User

  As a client
  I want to send DP896 manage user requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP896 successful responses between IIB and Azure
    Given I create the DP896 api payload for <condition>
    When  I send DP896 request to IIB endpoint
    And   I send DP896 request to Azure endpoint
    Then  I can see all the responses are identical for DP896

    Examples:
      | condition              |
      | transaction_successful |


  @negative
  Scenario Outline: Compare DP896 invalid responses between IIB and Azure
    Given I create the DP896 api payload for <condition>
    When  I send DP896 request to IIB endpoint
    And   I send DP896 request to Azure endpoint
    Then  I can see all the responses are identical for DP896

    Examples:
      | condition   |
      | missing_swn |
