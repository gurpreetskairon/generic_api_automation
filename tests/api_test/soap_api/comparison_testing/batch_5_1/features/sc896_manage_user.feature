@comparison
Feature: Comparison Testing - SC896 - Manage User

  As a client
  I want to send SC896 manage user requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC896 successful responses between IIB and Azure
    Given I create the SC896 api payload for <condition>
    When  I send SC896 request to IIB endpoint
    And   I send SC896 request to Azure endpoint
    Then  I can see all the responses are identical for SC896

    Examples:
      | condition              |
      | transaction_successful |


  @negative
  Scenario Outline: Compare SC896 invalid responses between IIB and Azure
    Given I create the SC896 api payload for <condition>
    When  I send SC896 request to IIB endpoint
    And   I send SC896 request to Azure endpoint
    Then  I can see all the responses are identical for SC896

    Examples:
      | condition   |
      | missing_swn |
