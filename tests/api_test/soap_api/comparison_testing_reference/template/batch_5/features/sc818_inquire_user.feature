@comparison
Feature: Comparison Testing - SC818 - Inquire User

  As a client
  I want to send SC818 inquire user requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC818 successful responses between IIB and Azure
    Given I create the SC818 api payload for <condition>
    When  I send SC818 request to IIB endpoint
    And   I send SC818 request to Azure endpoint
    Then  I can see all the responses are identical for SC818

    Examples:
      | condition           |
      | successful_response |
