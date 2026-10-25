@comparison
Feature: Comparison Testing - SC832 - Manage Communication

  As a client
  I want to send SC832 manage communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC832 successful responses between IIB and Azure
    Given I create the SC832 api payload for <condition>
    When  I send SC832 request to IIB endpoint
    And   I send SC832 request to Azure endpoint
    Then  I can see all the responses are identical for SC832

    Examples:
      | condition           |
      | successful_response |
