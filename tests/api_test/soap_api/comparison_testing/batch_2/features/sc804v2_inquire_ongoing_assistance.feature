@IIB-AZURE-COMPARISON @SOAP-API @sc804v2-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC804V2 - Inquire ongoing assistance

  As a client
  I want to compare the responses from the IIB and Azure for SC804-v1
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare SC804v2 successful response
    Given I create the correct api payload with <client_type>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | client_type       |
      | JS_WITH_AS        |
      | SPS_CURRENT       |
      | INACTIVE_SERVICES |


  @negative
  Scenario Outline: Compare SC804v2 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions            |
      | no_matching_record    |
      | client_not_recognised |
      | invalid_request       |
