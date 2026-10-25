@comparison
Feature: Comparison Testing - SC156 - Manage Proxy Engagement

  As a client
  I want to send SC156 manage proxy engagement requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC156 successful responses between IIB and Azure
    Given I create the SC156 api payload for <condition>
    When  I send SC156 request to IIB endpoint
    And   I send SC156 request to Azure endpoint
    Then  I can see all the responses are identical for SC156

    Examples:
      | condition |
      | create    |
      | delete    |
