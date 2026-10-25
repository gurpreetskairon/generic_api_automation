@comparison
Feature: Comparison Testing - SC880 - Manage Application

  As a client
  I want to send SC880 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC880 successful responses between IIB and Azure
    Given I create the SC880 api payload for <condition>
    When  I send SC880 request to IIB endpoint
    And   I send SC880 request to Azure endpoint
    Then  I can see all the responses are identical for SC880

    Examples:
      | condition                 |
      | transaction_successful    |
      | transaction_unsuccessful  |


  @negative
  Scenario Outline: Compare SC880 successful responses between IIB and Azure for negative scenarios
    Given I create the SC880 api payload for <condition>
    When  I send SC880 request to IIB endpoint
    And   I send SC880 request to Azure endpoint
    Then  I can see all the responses are identical for SC880

    Examples:
      | condition                 |
      | user_not_recognised       |
      | invalid_request           |
