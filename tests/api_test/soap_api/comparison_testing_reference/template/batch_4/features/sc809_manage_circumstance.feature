@comparison
Feature: Comparison Testing - SC809 - Manage Circumstance

  As a client
  I want to send SC809 manage circumstance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC809 successful responses between IIB and Azure
    Given I create the SC809 api payload for <condition>
    When  I send SC809 request to IIB endpoint
    And   I send SC809 request to Azure endpoint
    Then  I can see all the responses are identical for SC809

    Examples:
      | condition           |
      | successful_response |
