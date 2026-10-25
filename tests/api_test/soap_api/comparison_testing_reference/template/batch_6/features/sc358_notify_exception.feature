@comparison
Feature: Comparison Testing - SC358 - Notify Exception

  As a client
  I want to send SC358 notify exception requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC358 successful responses between IIB and Azure
    Given I create the SC358 api payload for <condition>
    When  I send SC358 request to IIB endpoint
    And   I send SC358 request to Azure endpoint
    Then  I can see all the responses are identical for SC358

    Examples:
      | condition           |
      | successful_response |
