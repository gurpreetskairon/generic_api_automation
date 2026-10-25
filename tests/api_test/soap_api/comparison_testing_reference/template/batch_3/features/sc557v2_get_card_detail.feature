@comparison
Feature: Comparison Testing - SC557v2 - Get Card Detail

  As a client
  I want to send SC557v2 get card detail requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC557v2 successful responses between IIB and Azure
    Given I create the SC557v2 api payload for <condition>
    When  I send SC557v2 request to IIB endpoint
    And   I send SC557v2 request to Azure endpoint
    Then  I can see all the responses are identical for SC557v2

    Examples:
      | condition           |
      | successful_response |
