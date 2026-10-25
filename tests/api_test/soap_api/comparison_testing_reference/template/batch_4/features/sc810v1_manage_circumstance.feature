@comparison
Feature: Comparison Testing - SC810V1 - Manage Circumstance

  As a client
  I want to send SC810V1 manage circumstance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC810V1 successful responses between IIB and Azure
    Given I create the SC810V1 api payload for <condition>
    When  I send SC810V1 request to IIB endpoint
    And   I send SC810V1 request to Azure endpoint
    Then  I can see all the responses are identical for SC810V1

    Examples:
      | condition           |
      | successful_response |
