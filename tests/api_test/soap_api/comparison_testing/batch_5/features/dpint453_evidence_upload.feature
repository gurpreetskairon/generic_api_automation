@IIB-AZURE-COMPARISON @SOAP-API @DP812-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - DPINT453 - evidence upload

  As a client
  I want to compare the responses from the IIB and Azure for DP812
  So that I can see whether the responses are identical



  @positive
  Scenario Outline: Compare dpint453 successful response for uploading documents
    Given I create the api payload with different <conditions> for <method> method
    And   I send a <method> request to the IIB endpoint
    And   I send a <method> request to Azure endpoint
    Then  I can see the responses are identical
    Examples:
    | conditions                  | method |
    | transaction_successful      | POST   |



  @positive
  Scenario Outline: Compare dpint453 successful response for deleting documents
    Given I create the api payload with different <conditions> for <method> method
    And   I send a <method> request to the IIB endpoint
    And   I send a <method> request to Azure endpoint
    Then  I can see the responses are identical
    Examples:
    | conditions                  | method |
    | delete_successful           | DELETE |
    | delete_unsuccessful         | DELETE |
