@comparison
Feature: Comparison Testing - DP861 - Inquire Client Appointments

  As a client
  I want to send DP861 inquire appointment requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP861 successful responses between IIB and Azure
    Given I create the DP861 api payload for <condition>
    When  I send DP861 request to IIB endpoint
    And   I send DP861 request to Azure endpoint
    Then  I can see all the responses are identical for DP861

    Examples:
      | condition                                    |
      | transaction_successful_appointments_found    |
      | transaction_successful_no_appointments_found |


  @negative
  Scenario Outline: Compare DP861 successful responses between IIB and Azure with an invalid swn
    Given I create the DP861 api payload for <condition>
    When  I send DP861 request to IIB endpoint
    And   I send DP861 request to Azure endpoint
    Then  I can see all the responses are identical for DP861

    Examples:
      | condition               |
      | invalid_request_data    |
