@comparison
Feature: Comparison Testing - SC815 - Manage User

  As a client
  I want to send SC815 manage user requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC815 successful responses between IIB and Azure
    Given I create the SC815 api payload for <condition>
    When  I send SC815 request to IIB endpoint
    And   I send SC815 request to Azure endpoint
    Then  I can see all the responses are identical for SC815

    Examples:
      | condition           |
      | successful_response |
