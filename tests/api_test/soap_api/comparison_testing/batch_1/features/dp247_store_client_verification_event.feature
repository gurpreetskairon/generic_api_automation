@SOAP-API
@DP247-comparison
Feature: Comparison Testing - DP247 - Store client verification event

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario: Compare DP247 successful responses
    Given I create the correct api payload
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical


  @positive
  Scenario Outline: Compare DP247 responses for no matching clients
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions         |
      | no_matching_client |


  @negative
  Scenario Outline: Compare DP247 responses with invalid data
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions                 |
      | user_not_recognised        |
      | invalid_transactionid      |
      | invalid_system             |
      | invalid_documenttypecode   |
      | invalid_dateOfBirthStatus  |
      | invalid_firstNameStatus    |
      | invalid_familyNameStatus   |
      | invalid_docStatus          |
      | invalid_livenesspassstatus |


  @negative
  Scenario Outline: Compare DP247 responses with an invalid client number
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions            |
      | invalid_client_number |
