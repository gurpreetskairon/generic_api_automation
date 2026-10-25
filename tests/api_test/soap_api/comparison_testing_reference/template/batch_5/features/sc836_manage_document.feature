@comparison
Feature: Comparison Testing - SC836 - Manage Document

  As a client
  I want to send SC836 manage document requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC836 successful responses between IIB and Azure
    Given I create the SC836 api payload for <condition>
    When  I send SC836 request to IIB endpoint
    And   I send SC836 request to Azure endpoint
    Then  I can see all the responses are identical for SC836

    Examples:
      | condition         |
      | birth_certificate |
      | passport          |
      | driver_licence    |
