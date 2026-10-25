@comparison
Feature: Comparison Testing - SC540 - Notify Expired Payment Instructions

  As a client
  I want to send SC540 notify expired payment instructions requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC540 successful responses between IIB and Azure
    Given I create the SC540 api payload for <condition>
    When  I send SC540 request to IIB endpoint
    And   I send SC540 request to Azure endpoint
    Then  I can see all the responses are identical for SC540

    Examples:
      | condition           |
      | successful_response |
