@comparison
Feature: Comparison Testing - SC347 - Advise Vacancy Match

  As a client
  I want to send SC347 advise vacancy match requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC347 successful responses between IIB and Azure
    Given I create the SC347 api payload for <condition>
    When  I send SC347 request to IIB endpoint
    And   I send SC347 request to Azure endpoint
    Then  I can see all the responses are identical for SC347

    Examples:
      | condition           |
      | successful_response |
