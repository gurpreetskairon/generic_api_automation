@comparison
Feature: Comparison Testing - SC834 - Manage Communication

  As a client
  I want to send SC834 manage communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC834 successful responses between IIB and Azure
    Given I create the SC834 api payload for <condition>
    When  I send SC834 request to IIB endpoint
    And   I send SC834 request to Azure endpoint
    Then  I can see all the responses are identical for SC834 with <condition>

    Examples:
      | condition             |
      | successful_response   |
      | no_notification_found |


  @negative
  Scenario Outline: Compare SC834 negative response between IIB and Azure
    Given I create the SC834 api payload for <condition>
    When  I send SC834 request to IIB endpoint
    And   I send SC834 request to Azure endpoint
    Then  I can see all the responses are identical for SC834 with <condition>

    Examples:
      | condition                   |
      | notification_not_recognised |
