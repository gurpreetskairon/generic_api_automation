@comparison
Feature: Comparison Testing - SC892 - Inquire Application

  As a client
  I want to send SC892 inquire application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC892 successful responses between IIB and Azure
    Given I create the SC892 api payload for <condition>
    When  I send SC892 request to IIB endpoint
    And   I send SC892 request to Azure endpoint
    Then  I can see all the responses are identical for SC892

    Examples:
      | condition           |
      | successful_response |
