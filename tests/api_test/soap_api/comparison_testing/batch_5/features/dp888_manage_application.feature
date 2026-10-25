@comparison
Feature: Comparison Testing - DP888 - Manage Application

  As a client
  I want to send DP888 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP888 successful responses between IIB and Azure for id verification
    Given I create the api payload with <application_consent>, <relationship_confirmation> and <application_verification> for <condition>
    When  I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see all the responses are identical for DP888

    Examples:
    | application_consent | relationship_confirmation | application_verification | condition |
    | ACCEPTED            | ACCEPTED                  | PROVIDED                 | NONE      |
    | ACCEPTED            | ACCEPTED                  | CANNOTPROVIDE            | NONE      |
    | ACCEPTED            | ACCEPTED                  | CANNOTNODOCS             | NONE      |
    | ACCEPTED            | ACCEPTED                  | ACCEPTBRING              | NONE      |
    | ACCEPTED            | REJECTED                  | PROVIDED                 | NONE      |
    | ACCEPTED            | REJECTED                  | CANNOTPROVIDE            | NONE      |
    | ACCEPTED            | REJECTED                  | CANNOTNODOCS             | NONE      |
    | ACCEPTED            | REJECTED                  | ACCEPTBRING              | NONE      |
    | ACCEPTED            | NODECISION                | PROVIDED                 | NONE      |
    | ACCEPTED            | NODECISION                | CANNOTPROVIDE            | NONE      |
    | ACCEPTED            | NODECISION                | CANNOTNODOCS             | NONE      |
    | ACCEPTED            | NODECISION                | ACCEPTBRING              | NONE      |
    | DISCUSS             | ACCEPTED                  | PROVIDED                 | NONE      |
    | DISCUSS             | ACCEPTED                  | CANNOTPROVIDE            | NONE      |
    | DISCUSS             | ACCEPTED                  | CANNOTNODOCS             | NONE      |
    | DISCUSS             | ACCEPTED                  | ACCEPTBRING              | NONE      |
    | DISCUSS             | REJECTED                  | PROVIDED                 | NONE      |
    | DISCUSS             | REJECTED                  | CANNOTPROVIDE            | NONE      |
    | DISCUSS             | REJECTED                  | CANNOTNODOCS             | NONE      |
    | DISCUSS             | REJECTED                  | ACCEPTBRING              | NONE      |
    | DISCUSS             | NODECISION                | PROVIDED                 | NONE      |
    | DISCUSS             | NODECISION                | CANNOTPROVIDE            | NONE      |
    | DISCUSS             | NODECISION                | CANNOTNODOCS             | NONE      |
    | DISCUSS             | NODECISION                | ACCEPTBRING              | NONE      |


  @negative
  Scenario Outline: Compare DP888 successful responses between IIB and Azure for negative scenarios
    Given I create the api payload with <application_consent>, <relationship_confirmation> and <application_verification> for <condition>
    When I send the request to IIB endpoint
    And I send the request to Azure endpoint
    Then I can see all the responses are identical for DP888

    Examples:
    | application_consent | relationship_confirmation | application_verification | condition                |
    | ACCEPTED            | ACCEPTED                  | PROVIDED                 | transaction_unsuccessful |
    | ACCEPTED            | ACCEPTED                  | PROVIDED                 | invalid_request   |
#    | ACCEPTED            | ACCEPTED                  | PROVIDED                 | schema_validation |
