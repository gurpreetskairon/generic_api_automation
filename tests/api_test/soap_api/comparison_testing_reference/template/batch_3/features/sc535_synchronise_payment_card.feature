@comparison
Feature: Comparison Testing - SC535 - Synchronise Payment Card

  As a client
  I want to send SC535 synchronise payment card requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC535 successful responses between IIB and Azure
    Given I create the SC535 api payload for <condition>
    When  I send SC535 request to IIB endpoint
    And   I send SC535 request to Azure endpoint
    Then  I can see all the responses are identical for SC535

    Examples:
      | condition           |
      | successful_response |
