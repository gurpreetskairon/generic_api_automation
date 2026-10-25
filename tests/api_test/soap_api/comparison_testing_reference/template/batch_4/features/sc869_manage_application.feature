@comparison
Feature: Comparison Testing - SC869 - Manage Application

  As a client
  I want to send SC869 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC869 successful responses between IIB and Azure
    Given I create the SC869 api payload for <condition>
    When  I send SC869 request to IIB endpoint
    And   I send SC869 request to Azure endpoint
    Then  I can see all the responses are identical for SC869

    Examples:
      | condition           |
      | successful_response |
