@comparison
Feature: Comparison Testing - SC835 - Manage Communication

  As a client
  I want to send SC835 manage communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC835 successful responses between IIB and Azure
    Given I create the SC835 api payload for <condition>
    When  I send SC835 request to IIB endpoint
    And   I send SC835 request to Azure endpoint
    Then  I can see all the responses are identical for SC835

    Examples:
      | condition           |
      | successful_response |
