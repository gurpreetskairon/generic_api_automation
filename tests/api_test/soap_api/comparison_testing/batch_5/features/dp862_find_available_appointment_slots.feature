@comparison
Feature: Comparison Testing - DP862 - find available appointment slots

  As a client
  I want to send DP862 find available appointment slots to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP862 successful responses between IIB and Azure
    Given I create the DP862 api payload for <condition>
    When  I send DP862 request to IIB endpoint
    And   I send DP862 request to Azure endpoint
    Then  I can see all the responses are identical for DP862

    Examples:
      | condition                  |
      | appointment_slots_found    |
      | no_appointment_slots_found |

  @negative
  Scenario Outline: Compare DP862 negative response between IIB and Azure
    Given I create the DP862 api payload for <condition>
    When  I send DP862 request to IIB endpoint
    And   I send DP862 request to Azure endpoint
    Then  I can see all the responses are identical for DP862

    Examples:
      | condition                  |
      | error_400_bad_request      |
