@comparison
Feature: Comparison Testing - SC891 - Assistance Aggregate

  As a client
  I want to send SC891 assistance aggregate requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC891 successful responses between IIB and Azure
    Given I create the SC891 api payload for <condition>
    When  I send SC891 request to IIB endpoint
    And   I send SC891 request to Azure endpoint
    Then  I can see all the responses are identical for SC891

    Examples:
      | condition           |
      | successful_response |
