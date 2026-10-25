@SOAP-API
Feature: Comparison Testing - SC826 - Find Client

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC826 successful response
    Given I create the correct api payload <payload_type>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | payload_type |
      | all_but_ird  |
      | dob_only     |
      | full_name    |
      | ird_only     |
      | name_gender  |


  #The below script requires a secured client


  @positive
  Scenario Outline: Compare SC826 responses with a secured client
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | payload_type | conditions     |
      | all_but_ird  | secured_client |
      | dob_only     | secured_client |
      | full_name    | secured_client |
      | ird_only     | secured_client |
      | name_gender  | secured_client |


  @negative
  Scenario Outline: Compare SC826 responses with invalid data
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | payload_type | conditions     |
      | all_but_ird  | invalid_gender |
      | all_but_ird  | invalid_name   |
      | ird_only     | invalid_ird    |
      | full_name    | invalid_name   |
      | name_gender  | invalid_gender |


  @negative
  Scenario Outline: Compare SC826 responses with invalid user
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | payload_type | conditions   |
      | all_but_ird  | invalid_user |
      | dob_only     | invalid_user |
      | ird_only     | invalid_user |
      | full_name    | invalid_user |
      | name_gender  | invalid_user |


  #The below script requires the environment to have 51 or more clients that share the same
  #names, gender and date of birth"""


  @negative
  Scenario Outline: Compare SC826 responses with results containing more than 50 entries
    Given I create the correct api payload <payload_type> with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | payload_type | conditions |
      | all_but_ird  | 50+Clients |
      | full_name    | 50+Clients |
      | name_gender  | 50+Clients |
