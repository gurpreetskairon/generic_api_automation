@AZURE-SOAP-API @SOAP-API @sc886-comparison
Feature: Comparison Testing - SC886 - Inquire Ongoing Applications

  As a client
  I want to send SC886 inquire ongoing applications requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 88600 - Transaction Successful
      * 88601 - No matching record
      * 88609 - User not recognised
      * 88610 - Invalid Request
      * 88611 - Client not recognised


  @positive @sc886-positive
  Scenario Outline: Compare SC886 successful responses between IIB and Azure
    Given I create the SC886 api payload for <condition>
    When  I send SC886 request to IIB endpoint
    And   I send SC886 request to Azure endpoint
    Then  I can see all the responses are identical for SC886

    Examples:
      | condition                    |
      | ongoing_application_found    |
      | no_ongoing_application_found |


  @negative @sc886-negative
  Scenario Outline: Compare SC886 unsuccessful responses between IIB and Azure
    Given I create the SC886 api payload for <condition>
    When  I send SC886 request to IIB endpoint
    And   I send SC886 request to Azure endpoint
    Then  I can see all the responses are identical for SC886

    Examples:
      | condition             |
      | user_not_recognised   |
      | invalid_request       |
      | client_not_recognised |
