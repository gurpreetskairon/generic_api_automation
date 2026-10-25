@REST-API
Feature: Comparison Testing - SC934 - Inquire Outbound Campaign Status

  As a client,
  I want to send SC934 Inquire Outbound Campaign Status requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes and messages are:
      * 93400 - Request was successful
      * 93440 - Invalid Request


  @positive
  Scenario Outline: Compare SC934 successful transaction response
    Given I create the correct SC934 api request with different <conditions>
    And   I send the SC934 request to IIB endpoint
    And   I send the SC934 request to Azure endpoint
    Then  I can see all the responses are identical for SC934

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC934 invalid request response
    Given I create the correct SC934 api request with different <conditions>
    And   I send the SC934 request to IIB endpoint
    And   I send the SC934 request to Azure endpoint
    Then  I can see all the responses are identical for SC934

    Examples:
      | conditions      |
      | invalid_request |
