@comparison
Feature: Comparison Testing - SC348 - Confirm Application Referral

  As a client
  I want to send SC348 confirm application referral requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC348 successful responses between IIB and Azure
    Given I create the SC348 api payload for <condition>
    When  I send SC348 request to IIB endpoint
    And   I send SC348 request to Azure endpoint
    Then  I can see all the responses are identical for SC348

    Examples:
      | condition           |
      | successful_response |
