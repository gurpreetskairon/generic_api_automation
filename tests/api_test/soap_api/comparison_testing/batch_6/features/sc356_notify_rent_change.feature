@AZURE-SOAP-API @SOAP-API @sc356-comparison
Feature: Comparison Testing - SC356 - Notify Rent Change

  As a client,
  I want to send SC356 Notify Rent Change requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 35600 - Success
      * 35601 - Invalid request


  @positive
  @sc356-positive
  Scenario Outline: Compare SC356 successful responses between IIB and Azure
    Given I create the SC356 api payload for <condition>
    When  I send SC356 request to IIB endpoint
    And   I send SC356 request to Azure endpoint
    Then  I can see all the responses are identical for SC356

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc356-negative
  Scenario Outline: Compare SC356 unsuccessful responses between IIB and Azure
    Given I create the SC356 api payload for <condition>
    When  I send SC356 request to IIB endpoint
    And   I send SC356 request to Azure endpoint
    Then  I can see all the responses are identical for SC356

    Examples:
      | condition       |
      | invalid_request |
