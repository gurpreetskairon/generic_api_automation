@comparison
Feature: Comparison Testing - SC887 - Inquire Application

  As a client
  I want to send SC887 inquire application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC887 successful responses between IIB and Azure
    Given I create the SC887 api payload for <condition>
    When  I send SC887 request to IIB endpoint
    And   I send SC887 request to Azure endpoint
    Then  I can see all the responses are identical for SC887

    Examples:
      | condition           |
      | successful_response |
