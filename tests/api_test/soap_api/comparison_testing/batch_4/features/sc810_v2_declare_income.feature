@SOAP-API
Feature: Comparison Testing - SC810V2 - Declare Income

  As a client,
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC810V2 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC810V2 successful transaction response
    Given I create the correct SC810V2 api payload with different <conditions>
    And   I send the SC810V2 request to IIB endpoint
    And   I send the SC810V2 request to Azure endpoint
    Then  I can see all the responses are identical for SC810V2

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC810V2 unsuccessful transaction responses
    Given I create the correct SC810V2 api payload with different <conditions>
    And   I send the SC810V2 request to IIB endpoint
    And   I send the SC810V2 request to Azure endpoint
    Then  I can see all the responses are identical for SC810V2

    Examples:
      | conditions                        |
      | client_not_recognised             |
      | income_record_already_held        |
      | client_not_receiving_main_benefit |
