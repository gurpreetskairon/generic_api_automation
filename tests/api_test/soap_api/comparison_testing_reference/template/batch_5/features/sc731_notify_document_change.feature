@comparison
Feature: Comparison Testing - SC731 - Notify Document Change

  As a client
  I want to send SC731 notify document change requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC731 successful responses between IIB and Azure
    Given I create the SC731 api payload for <condition>
    When  I send SC731 request to IIB endpoint
    And   I send SC731 request to Azure endpoint
    Then  I can see all the responses are identical for SC731

    Examples:
      | condition           |
      | successful_response |
