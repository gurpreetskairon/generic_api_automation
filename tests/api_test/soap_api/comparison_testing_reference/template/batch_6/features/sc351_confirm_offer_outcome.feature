@comparison
Feature: Comparison Testing - SC351 - Confirm Offer Outcome

  As a client
  I want to send SC351 confirm offer outcome requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC351 successful responses between IIB and Azure
    Given I create the SC351 api payload for <condition>
    When  I send SC351 request to IIB endpoint
    And   I send SC351 request to Azure endpoint
    Then  I can see all the responses are identical for SC351

    Examples:
      | condition           |
      | successful_response |
