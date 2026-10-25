@comparison
Feature: Comparison Testing - SC356 - Notify Rent Change

  As a client
  I want to send SC356 notify rent change requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC356 successful responses between IIB and Azure
    Given I create the SC356 api payload for <condition>
    When  I send SC356 request to IIB endpoint
    And   I send SC356 request to Azure endpoint
    Then  I can see all the responses are identical for SC356

    Examples:
      | condition           |
      | successful_response |
