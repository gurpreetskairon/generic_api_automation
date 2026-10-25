@comparison
Feature: Comparison Testing - SC877 - Manage Circumstance

  As a client
  I want to send SC877 manage circumstance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC877 successful responses between IIB and Azure
    Given I create the SC877 api payload for <condition>
    When  I send SC877 request to IIB endpoint
    And   I send SC877 request to Azure endpoint
    Then  I can see all the responses are identical for SC877

    Examples:
      | condition           |
      | successful_response |
