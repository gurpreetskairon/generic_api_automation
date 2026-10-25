@comparison
Feature: Comparison Testing - SC730 - Notify Document Store

  As a client
  I want to send SC730 notify document store requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC730 successful responses between IIB and Azure
    Given I create the SC730 api payload for <condition>
    When  I send SC730 request to IIB endpoint
    And   I send SC730 request to Azure endpoint
    Then  I can see all the responses are identical for SC730

    Examples:
      | condition           |
      | successful_response |
