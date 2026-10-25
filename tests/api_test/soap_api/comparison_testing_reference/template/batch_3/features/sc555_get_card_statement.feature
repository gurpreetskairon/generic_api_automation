@comparison
Feature: Comparison Testing - SC555 - Get Card Statement

  As a client
  I want to send SC555 get card statement requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC555 successful responses between IIB and Azure
    Given I create the SC555 api payload for <condition>
    When  I send SC555 request to IIB endpoint
    And   I send SC555 request to Azure endpoint
    Then  I can see all the responses are identical for SC555

    Examples:
      | condition           |
      | successful_response |
