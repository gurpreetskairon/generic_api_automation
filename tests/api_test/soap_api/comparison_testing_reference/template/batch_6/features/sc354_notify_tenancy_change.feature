@comparison
Feature: Comparison Testing - SC354 - Notify Tenancy Change

  As a client
  I want to send SC354 notify tenancy change requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC354 successful responses between IIB and Azure
    Given I create the SC354 api payload for <condition>
    When  I send SC354 request to IIB endpoint
    And   I send SC354 request to Azure endpoint
    Then  I can see all the responses are identical for SC354

    Examples:
      | condition           |
      | successful_response |
