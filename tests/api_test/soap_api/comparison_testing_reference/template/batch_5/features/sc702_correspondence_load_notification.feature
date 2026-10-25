@comparison
Feature: Comparison Testing - SC702 - Correspondence Load Notification

  As a client
  I want to send SC702 correspondence load notification requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC702 successful responses between IIB and Azure
    Given I create the SC702 api payload for <condition>
    When  I send SC702 request to IIB endpoint
    And   I send SC702 request to Azure endpoint
    Then  I can see all the responses are identical for SC702

    Examples:
      | condition           |
      | successful_response |
