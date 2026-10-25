@AZURE-SOAP-API @SOAP-API @sc343-comparison
Feature: Comparison Testing - SC343 - Notify Adhoc Event

  As a client,
  I want to send SC343 Notify Adhoc Event requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected response conditions are:
      * Acknowledged message received - Success
      * Invalid request - HTTP 400, Schema Validation Error (A2A or B2B)
      * SWN is not recognised by MSD as belonging to a tenant or partner of the housing supplier - provide error
      * Authentication failure - HTTP 400
      * Message code is not recognised as a valid code - Unsuccessful


  @positive
  @sc343-positive
  Scenario Outline: Compare SC343 successful responses between IIB and Azure
    Given I create the SC343 api payload for <condition>
    When  I send SC343 request to IIB endpoint
    And   I send SC343 request to Azure endpoint
    Then  I can see all the responses are identical for SC343

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc343-negative
  Scenario Outline: Compare SC343 unsuccessful responses between IIB and Azure
    Given I create the SC343 api payload for <condition>
    When  I send SC343 request to IIB endpoint
    And   I send SC343 request to Azure endpoint
    Then  I can see all the responses are identical for SC343

    Examples:
      | condition                   |
      | invalid_request             |
      | swn_not_recognised          |
      | authentication_failure      |
      | message_code_not_recognised |
