@comparison
Feature: Comparison Testing - SC556 - Get Card Transaction

  As a client
  I want to send SC556 get card transaction requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC556 successful responses between IIB and Azure
    Given I create the SC556 api payload for <condition>
    When  I send SC556 request to IIB endpoint
    And   I send SC556 request to Azure endpoint
    Then  I can see all the responses are identical for SC556

    Examples:
      | condition           |
      | successful_response |
