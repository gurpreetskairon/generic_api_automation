@comparison
Feature: Comparison Testing - SC890 - Assistance Aggregate

  As a client
  I want to send SC890 assistance aggregate requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC890 successful responses between IIB and Azure
    Given I create the SC890 api payload for <condition>
    When  I send SC890 request to IIB endpoint
    And   I send SC890 request to Azure endpoint
    Then  I can see all the responses are identical for SC890

    Examples:
      | condition           |
      | successful_response |
