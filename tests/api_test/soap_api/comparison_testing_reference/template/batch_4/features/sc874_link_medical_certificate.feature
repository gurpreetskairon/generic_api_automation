@comparison
Feature: Comparison Testing - SC874 - Link Medical Certificate

  As a client
  I want to send SC874 link medical certificate requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC874 successful responses between IIB and Azure
    Given I create the SC874 api payload for <condition>
    When  I send SC874 request to IIB endpoint
    And   I send SC874 request to Azure endpoint
    Then  I can see all the responses are identical for SC874

    Examples:
      | condition           |
      | successful_response |
