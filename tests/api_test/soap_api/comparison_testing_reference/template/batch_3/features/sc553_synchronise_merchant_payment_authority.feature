@comparison
Feature: Comparison Testing - SC553 - Synchronise Merchant Payment Authority

  As a client
  I want to send SC553 synchronise merchant payment authority requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC553 successful responses between IIB and Azure
    Given I create the SC553 api payload for <condition>
    When  I send SC553 request to IIB endpoint
    And   I send SC553 request to Azure endpoint
    Then  I can see all the responses are identical for SC553

    Examples:
      | condition           |
      | successful_response |
