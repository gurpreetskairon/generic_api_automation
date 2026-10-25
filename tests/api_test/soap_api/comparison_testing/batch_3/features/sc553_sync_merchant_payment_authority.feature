@SOAP-API
Feature: Comparison Testing - SC553 - Sync Merchant Payment Authority

  As a client
  I want to send SC553 requests to IIB and Azure
  So that I can compare the responses from both endpoints


  @positive
  Scenario Outline: Compare SC553 successful transaction response
    Given I create the correct SC553 api payload with different <conditions>
    And   I send the SC553 request to IIB endpoint
    And   I send the SC553 request to Azure endpoint
    Then  I can see all the responses are identical for SC553

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC553 unsuccessful transaction responses
    Given I create the correct SC553 api payload with different <conditions>
    And   I send the SC553 request to IIB endpoint
    And   I send the SC553 request to Azure endpoint
    Then  I can see all the responses are identical for SC553

    Examples:
      | conditions          |
      | superseded_request  |
      | invalid_xml         |
      | invalid_merchant_id |
