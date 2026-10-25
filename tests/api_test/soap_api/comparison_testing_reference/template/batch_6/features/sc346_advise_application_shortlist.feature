@comparison
Feature: Comparison Testing - SC346 - Advise Application Shortlist

  As a client
  I want to send SC346 advise application shortlist requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC346 successful responses between IIB and Azure
    Given I create the SC346 api payload for <condition>
    When  I send SC346 request to IIB endpoint
    And   I send SC346 request to Azure endpoint
    Then  I can see all the responses are identical for SC346

    Examples:
      | condition           |
      | successful_response |
