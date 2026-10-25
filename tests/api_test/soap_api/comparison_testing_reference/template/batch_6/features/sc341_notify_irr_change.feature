@comparison
Feature: Comparison Testing - SC341 - Notify Irr Change

  As a client
  I want to send SC341 notify irr change requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC341 successful responses between IIB and Azure
    Given I create the SC341 api payload for <condition>
    When  I send SC341 request to IIB endpoint
    And   I send SC341 request to Azure endpoint
    Then  I can see all the responses are identical for SC341

    Examples:
      | condition           |
      | successful_response |
