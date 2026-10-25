@comparison
Feature: Comparison Testing - SC127 - Get Client Obligation Failure

  As a client
  I want to send SC127 get client obligation failure requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC127 successful responses between IIB and Azure
    Given I create the SC127 api payload for <condition>
    When  I send SC127 request to IIB endpoint
    And   I send SC127 request to Azure endpoint
    Then  I can see all the responses are identical for SC127

    Examples:
      | condition           |
      | successful_response |
