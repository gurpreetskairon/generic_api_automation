@AZURE-SOAP-API @SOAP-API @sc882-comparison
Feature: Comparison Testing - SC882 - Initiate Hardship Application Approval

  As a client
  I want to send SC882 initiate hardship application approval requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 88200 - Transaction Successful
      * 88201 - Transaction Unsuccessful
    * Invalid Request is also covered when the mandatory case reference is missing


  @positive @sc882-positive
  Scenario Outline: Compare SC882 successful responses between IIB and Azure
    Given I create the SC882 api payload for <condition>
    When  I send SC882 request to IIB endpoint
    And   I send SC882 request to Azure endpoint
    Then  I can see all the responses are identical for SC882

    Examples:
      | condition                 |
      | approval_request_received |


  @negative @sc882-negative
  Scenario Outline: Compare SC882 unsuccessful responses between IIB and Azure
    Given I create the SC882 api payload for <condition>
    When  I send SC882 request to IIB endpoint
    And   I send SC882 request to Azure endpoint
    Then  I can see all the responses are identical for SC882

    Examples:
      | condition                          |
      | unable_to_process_approval_request |
      | invalid_request                    |
