@comparison
Feature: Comparison Testing - SC862 - find available appointment slots

  As a client
  I want to send SC862 find available appointment slots to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC862 successful responses between IIB and Azure
    Given I create the SC862 api payload for <condition>
    When  I send SC862 request to IIB endpoint
    And   I send SC862 request to Azure endpoint
    Then  I can see all the responses are identical for SC862

    Examples:
      | condition                  |
      | appointment_slots_found    |
      | no_appointment_slots_found |

  @negative
  Scenario Outline: Compare SC862 negative response between IIB and Azure
    Given I create the SC862 api payload for <condition>
    When  I send SC862 request to IIB endpoint
    And   I send SC862 request to Azure endpoint
    Then  I can see all the responses are identical for SC862

    Examples:
      | condition                  |
      | error_400_bad_request      |
