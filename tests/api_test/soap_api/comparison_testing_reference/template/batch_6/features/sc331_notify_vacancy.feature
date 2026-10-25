@comparison
Feature: Comparison Testing - SC331 - Notify Vacancy

  As a client
  I want to send SC331 notify vacancy requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC331 successful responses between IIB and Azure
    Given I create the SC331 api payload for <condition>
    When  I send SC331 request to IIB endpoint
    And   I send SC331 request to Azure endpoint
    Then  I can see all the responses are identical for SC331

    Examples:
      | condition           |
      | successful_response |
