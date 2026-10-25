@comparison
Feature: Comparison Testing - SC560 - Set Payment Card Pin

  As a client
  I want to send SC560 set payment card pin requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC560 successful responses between IIB and Azure
    Given I create the SC560 api payload for <condition>
    When  I send SC560 request to IIB endpoint
    And   I send SC560 request to Azure endpoint
    Then  I can see all the responses are identical for SC560

    Examples:
      | condition           |
      | successful_response |
