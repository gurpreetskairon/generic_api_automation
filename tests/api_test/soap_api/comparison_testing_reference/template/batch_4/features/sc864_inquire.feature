@comparison
Feature: Comparison Testing - SC864 - Inquire

  As a client
  I want to send SC864 inquire requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC864 successful responses between IIB and Azure
    Given I create the SC864 api payload for <condition>
    When  I send SC864 request to IIB endpoint
    And   I send SC864 request to Azure endpoint
    Then  I can see all the responses are identical for SC864

    Examples:
      | condition           |
      | successful_response |
