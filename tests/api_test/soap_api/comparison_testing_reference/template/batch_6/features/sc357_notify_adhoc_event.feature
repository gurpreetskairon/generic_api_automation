@comparison
Feature: Comparison Testing - SC357 - Notify Adhoc Event

  As a client
  I want to send SC357 notify adhoc event requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC357 successful responses between IIB and Azure
    Given I create the SC357 api payload for <condition>
    When  I send SC357 request to IIB endpoint
    And   I send SC357 request to Azure endpoint
    Then  I can see all the responses are identical for SC357

    Examples:
      | condition           |
      | successful_response |
