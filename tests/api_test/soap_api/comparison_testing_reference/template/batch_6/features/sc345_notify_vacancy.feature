@comparison
Feature: Comparison Testing - SC345 - Notify Vacancy

  As a client
  I want to send SC345 notify vacancy requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC345 successful responses between IIB and Azure
    Given I create the SC345 api payload for <condition>
    When  I send SC345 request to IIB endpoint
    And   I send SC345 request to Azure endpoint
    Then  I can see all the responses are identical for SC345

    Examples:
      | condition           |
      | successful_response |
