@comparison
Feature: Comparison Testing - SC816 - Manage User

  As a client
  I want to send SC816 manage user requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC816 successful responses between IIB and Azure
    Given I create the SC816 api payload for <condition>
    When  I send SC816 request to IIB endpoint
    And   I send SC816 request to Azure endpoint
    Then  I can see all the responses are identical for SC816

    Examples:
      | condition           |
      | successful_response |
