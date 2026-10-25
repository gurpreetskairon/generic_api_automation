@IIB-AZURE-COMPARISON @SOAP-API @sc849-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC849 - Inquire provider user

  As a client
  I want to compare the responses from the IIB and Azure for SC849
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare SC849 successful response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions                     |
      | no_current_activities          |
      | one_or_more_current_activities |


  @negative
  Scenario Outline: Compare SC849 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions               |
      | alpha_numeric_swn        |
      | no_client_swn            |
      | activity_type_not_mapped |
