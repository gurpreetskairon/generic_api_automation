@comparison
Feature: Comparison Testing - SC868 - Manage Application

  As a client
  I want to send SC868 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC868 successful responses between IIB and Azure
    Given I create the SC868 api payload for <condition>
    When  I send SC868 request to IIB endpoint
    And   I send SC868 request to Azure endpoint
    Then  I can see all the responses are identical for SC868

    Examples:
      | condition           |
      | successful_response |
