@comparison
Feature: Comparison Testing - SC865 - Manage Circumstance

  As a client
  I want to send SC865 manage circumstance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC865 successful responses between IIB and Azure
    Given I create the SC865 api payload for <condition>
    When  I send SC865 request to IIB endpoint
    And   I send SC865 request to Azure endpoint
    Then  I can see all the responses are identical for SC865

    Examples:
      | condition           |
      | successful_response |
