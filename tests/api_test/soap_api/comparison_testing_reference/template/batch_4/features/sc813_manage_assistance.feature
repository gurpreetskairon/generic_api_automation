@comparison
Feature: Comparison Testing - SC813 - Manage Assistance

  As a client
  I want to send SC813 manage assistance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC813 successful responses between IIB and Azure
    Given I create the SC813 api payload for <condition>
    When  I send SC813 request to IIB endpoint
    And   I send SC813 request to Azure endpoint
    Then  I can see all the responses are identical for SC813

    Examples:
      | condition           |
      | successful_response |
