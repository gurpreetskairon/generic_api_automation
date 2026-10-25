@comparison
Feature: Comparison Testing - SC803 - Manage Assistance

  As a client
  I want to send SC803 manage assistance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC803 successful responses between IIB and Azure
    Given I create the SC803 api payload for <condition>
    When  I send SC803 request to IIB endpoint
    And   I send SC803 request to Azure endpoint
    Then  I can see all the responses are identical for SC803

    Examples:
      | condition           |
      | successful_response |
