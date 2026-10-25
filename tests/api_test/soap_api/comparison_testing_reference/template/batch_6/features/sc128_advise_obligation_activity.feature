@comparison
Feature: Comparison Testing - SC128 - Advise Obligation Activity

  As a client
  I want to send SC128 advise obligation activity requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC128 successful responses between IIB and Azure
    Given I create the SC128 api payload for <condition>
    When  I send SC128 request to IIB endpoint
    And   I send SC128 request to Azure endpoint
    Then  I can see all the responses are identical for SC128

    Examples:
      | condition           |
      | successful_response |
