@comparison
Feature: Comparison Testing - SC872 - Manage Application

  As a client
  I want to send SC872 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC872 successful responses between IIB and Azure
    Given I create the SC872 api payload for <condition>
    When  I send SC872 request to IIB endpoint
    And   I send SC872 request to Azure endpoint
    Then  I can see all the responses are identical for SC872

    Examples:
      | condition           |
      | successful_response |
