@comparison
Feature: Comparison Testing - SC882 - Manage Application

  As a client
  I want to send SC882 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC882 successful responses between IIB and Azure
    Given I create the SC882 api payload for <condition>
    When  I send SC882 request to IIB endpoint
    And   I send SC882 request to Azure endpoint
    Then  I can see all the responses are identical for SC882

    Examples:
      | condition           |
      | successful_response |
