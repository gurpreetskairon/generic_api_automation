@IIB-AZURE-COMPARISON @SOAP-API @sc811-v1-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC811V1 - Inquire Circumstance

  As a client
  I want to send SC811 V1 SOAP requests to both IIB and Azure
  So that I can confirm both endpoints return the same result.


  @positive
  Scenario Outline: Compare SC811 V1 successful transaction response
    Given I create the correct payload for SC811 V1 with "<condition>"
    And   I send the SC811 V1 request to IIB endpoint
    And   I send the SC811 V1 request to Azure endpoint
    Then  I can see all the responses are identical for SC811 V1

    Examples:
      | condition          |
      | success            |
      | no_matching_record |


  @negative
  Scenario Outline: Compare SC811 V1 unsuccessful transaction response
    Given I create the payload for SC811 V1 with "<condition>"
    And   I send the SC811 V1 request to IIB endpoint
    And   I send the SC811 V1 request to Azure endpoint
    Then  I can see all the responses are identical for SC811 V1

    Examples:
      | condition             |
      | invalid_request       |
      | client_not_recognised |
