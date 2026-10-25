@comparison
Feature: Comparison Testing - SC343 - Notify Adhoc Event

  As a client
  I want to send SC343 notify adhoc event requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC343 successful responses between IIB and Azure
    Given I create the SC343 api payload for <condition>
    When  I send SC343 request to IIB endpoint
    And   I send SC343 request to Azure endpoint
    Then  I can see all the responses are identical for SC343

    Examples:
      | condition           |
      | successful_response |
