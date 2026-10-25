@SOAP-API
Feature: Comparison Testing - SC809 - Advise Change of Housing Circumstance

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC809 responses are identical


  @positive
  Scenario Outline: Compare SC809 successful transaction response
    Given I create the correct SC809 api payload with different <conditions>
    And   I send the SC809 request to IIB endpoint
    And   I send the SC809 request to Azure endpoint
    Then  I can see all the responses are identical for SC809

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC809 unsuccessful transaction response
    Given I create the correct SC809 api payload with different <conditions>
    And   I send the SC809 request to IIB endpoint
    And   I send the SC809 request to Azure endpoint
    Then  I can see all the responses are identical for SC809

    Examples:
      | conditions            |
      | client_not_recognised |
      | invalid_message       |
