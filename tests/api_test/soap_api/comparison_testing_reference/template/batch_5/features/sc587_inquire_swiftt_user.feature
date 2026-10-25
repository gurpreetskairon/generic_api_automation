@comparison
Feature: Comparison Testing - SC587 - Inquire Swiftt User

  As a client
  I want to send SC587 inquire swiftt user requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC587 successful responses between IIB and Azure
    Given I create the SC587 api payload for <condition>
    When  I send SC587 request to IIB endpoint
    And   I send SC587 request to Azure endpoint
    Then  I can see all the responses are identical for SC587

    Examples:
      | condition           |
      | successful_response |
