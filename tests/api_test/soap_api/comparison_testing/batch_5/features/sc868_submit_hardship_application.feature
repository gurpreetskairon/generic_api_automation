@SOAP-API
Feature: Comparison Testing - SC868 - Submit Hardship Application

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC868 responses are identical


  @positive
  Scenario Outline: Compare SC868 successful transaction response
    Given I create the correct SC868 api payload with different <conditions>
    And   I send the SC868 request to IIB endpoint
    And   I send the SC868 request to Azure endpoint
    Then  I can see all the responses are identical for SC868

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC868 invalid request response
    Given I create the correct SC868 api payload with different <conditions>
    And   I send the SC868 request to IIB endpoint
    And   I send the SC868 request to Azure endpoint
    Then  I can see all the responses are identical for SC868

    Examples:
      | conditions      |
      | invalid_request |
