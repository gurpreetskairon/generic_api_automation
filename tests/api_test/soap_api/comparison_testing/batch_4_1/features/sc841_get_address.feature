
@AZURE-SOAP-API @SOAP-API @sc841-comparison
Feature: Comparison Testing - SC841 - Get Address
  As a client,
  I want to send SC841 Get Address requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 84100 - Transaction Successful (one address matches the query)
      * 84101 - No matching record (no address matches the query)
      * 84102 - Invalid request (an invalid request is submitted)
    * AddressId is not validated by this service

  @positive @sc841-positive
  Scenario Outline: Compare SC841 successful responses between IIB and Azure
    Given I create the SC841 api payload for <condition>
    When I send SC841 request to IIB endpoint
    And I send SC841 request to Azure endpoint
    Then I can see all the responses are identical for SC841

    Examples:
      | condition          |
      | matching_address   |
      | no_matching_record |

  @negative @sc841-negative
  Scenario Outline: Compare SC841 unsuccessful responses between IIB and Azure
    Given I create the SC841 api payload for <condition>
    When I send SC841 request to IIB endpoint
    And I send SC841 request to Azure endpoint
    Then I can see all the responses are identical for SC841

    Examples:
      | condition       |
      | invalid_request |
