@comparison
Feature: Comparison Testing - DP834 - Manage Communication

  As a client
  I want to send DP834 manage communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP834 successful responses between IIB and Azure
    Given I create the DP834 api payload for <condition>
    When  I send DP834 request to IIB endpoint
    And   I send DP834 request to Azure endpoint
    Then  I can see all the responses are identical for DP834

    Examples:
      | condition             |
      | successful_response   |
      | no_notification_found |


  @negative
  Scenario Outline: Compare DP834 negative response between IIB and Azure
    Given I create the DP834 api payload for <condition>
    When  I send DP834 request to IIB endpoint
    And   I send DP834 request to Azure endpoint
    Then  I can see all the responses are identical for DP834

    Examples:
      | condition                   |
      | notification_not_recognised |
