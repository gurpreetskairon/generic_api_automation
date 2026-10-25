@comparison
Feature: Comparison Testing - SC730V2 - Notify Document Store

  As a client
  I want to send SC730V2 notify document store requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC730V2 successful responses between IIB and Azure
    Given I create the SC730V2 api payload for <condition>
    When  I send SC730V2 request to IIB endpoint
    And   I send SC730V2 request to Azure endpoint
    Then  I can see all the responses are identical for SC730V2

    Examples:
      | condition           |
      | successful_response |
