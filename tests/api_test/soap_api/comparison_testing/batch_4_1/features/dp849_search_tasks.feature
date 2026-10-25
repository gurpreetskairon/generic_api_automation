@IIB-AZURE-COMPARISON @SOAP-API @dp849-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - DP849 - Inquire provider user

  As a client
  I want to compare the responses from the IIB and Azure for dp849
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare dp849 successful response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions                     |
      | no_current_activities          |
      | one_or_more_current_activities |


  @negative
  Scenario Outline: Compare dp849 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions            |
      | alpha_numeric_swn     |
      | invalid_client_number |
      | invalid_activity_code |
