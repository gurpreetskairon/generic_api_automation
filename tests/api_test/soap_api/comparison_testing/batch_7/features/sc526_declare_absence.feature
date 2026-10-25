@AZURE-SOAP-API @SOAP-API @sc526-comparison
Feature: Comparison Testing - SC526 - Declare Absence

  As a client,
  I want to send SC526 Declare Absence requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes and messages are:
      * 52600 - Transaction Successful
      * 52601 - Transaction Not Successful


  @positive
  Scenario Outline: Compare SC526 successful responses between IIB and Azure
    Given I create the SC526 api payload for <condition>
    When I send SC526 request to IIB endpoint
    And I send SC526 request to Azure endpoint
    Then I can see all the responses are identical for SC526

    Examples:
      | condition              |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC526 unsuccessful responses between IIB and Azure
    Given I create the SC526 api payload for <condition>
    When I send SC526 request to IIB endpoint
    And I send SC526 request to Azure endpoint
    Then I can see all the responses are identical for SC526

    Examples:
      | condition                |
      | unsuccessful_transaction |
