@comparison
Feature: Comparison Testing - SC846 - Manage Assistance

  As a client
  I want to send SC846 manage assistance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC846 successful responses between IIB and Azure
    Given I create the SC846 api payload for <condition>
    When  I send SC846 request to IIB endpoint
    And   I send SC846 request to Azure endpoint
    Then  I can see all the responses are identical for SC846

    Examples:
      | condition           |
      | successful_response |
