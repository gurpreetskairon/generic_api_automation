@comparison
Feature: Comparison Testing - SC802 - Manage Assistance

  As a client
  I want to send SC802 manage assistance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC802 successful responses between IIB and Azure
    Given I create the SC802 api payload for <condition>
    When  I send SC802 request to IIB endpoint
    And   I send SC802 request to Azure endpoint
    Then  I can see all the responses are identical for SC802

    Examples:
      | condition       |
      | change_payment  |
      | suspend_benefit |
