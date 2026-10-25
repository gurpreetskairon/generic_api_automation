@AZURE-SOAP-API @SOAP-API @sc342-comparison
Feature: Comparison Testing - SC342 - Notify Rent Change

  As a client,
  I want to send SC342 Notify Rent Change requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected response conditions are:
      * Successful request - Success
      * Invalid request - HTTP 400, Schema Validation Error (A2A or B2B)
      * Tenancy is not known to MSD - provide error
      * Authentication failure - HTTP 400
    * For a successful request, a response is formed without a response body


  @positive
  @sc342-positive
  Scenario Outline: Compare SC342 successful responses between IIB and Azure
    Given I create the SC342 api payload for <condition>
    When  I send SC342 request to IIB endpoint
    And   I send SC342 request to Azure endpoint
    Then  I can see all the responses are identical for SC342

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc342-negative
  Scenario Outline: Compare SC342 unsuccessful responses between IIB and Azure
    Given I create the SC342 api payload for <condition>
    When  I send SC342 request to IIB endpoint
    And   I send SC342 request to Azure endpoint
    Then  I can see all the responses are identical for SC342

    Examples:
      | condition              |
      | invalid_request        |
      | tenancy_not_known      |
      | authentication_failure |
