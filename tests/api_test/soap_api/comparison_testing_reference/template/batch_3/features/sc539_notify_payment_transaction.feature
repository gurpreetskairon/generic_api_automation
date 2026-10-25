@comparison
Feature: Comparison Testing - SC539 - Notify Payment Transaction

  As a client
  I want to send SC539 notify payment transaction requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC539 successful responses between IIB and Azure
    Given I create the SC539 api payload for <condition>
    When  I send SC539 request to IIB endpoint
    And   I send SC539 request to Azure endpoint
    Then  I can see all the responses are identical for SC539

    Examples:
      | condition           |
      | successful_response |
