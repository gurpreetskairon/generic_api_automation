@comparison
Feature: Comparison Testing - SC812 - Inquire Entitlement

  As a client
  I want to send SC812 inquire entitlement requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC812 successful responses between IIB and Azure
    Given I create the SC812 api payload for <condition>
    When  I send SC812 request to IIB endpoint
    And   I send SC812 request to Azure endpoint
    Then  I can see all the responses are identical for SC812

    Examples:
      | condition           |
      | successful_response |
