@comparison
Feature: Comparison Testing - SC886 - Inquire Application

  As a client
  I want to send SC886 inquire application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC886 successful responses between IIB and Azure
    Given I create the SC886 api payload for <condition>
    When  I send SC886 request to IIB endpoint
    And   I send SC886 request to Azure endpoint
    Then  I can see all the responses are identical for SC886

    Examples:
      | condition           |
      | successful_response |
