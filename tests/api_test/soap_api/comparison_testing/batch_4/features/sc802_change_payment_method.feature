@SOAP-API
Feature: Comparison Testing - SC802 - Change Payment Method

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC802 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC802 successful transaction response
    Given I create the correct SC802 api payload with different <conditions>
    And   I send the SC802 request to IIB endpoint
    And   I send the SC802 request to Azure endpoint
    Then  I can see all the responses are identical for SC802

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC802 unsuccessful transaction response
    Given I create the correct SC802 api payload with different <conditions>
    And   I send the SC802 request to IIB endpoint
    And   I send the SC802 request to Azure endpoint
    Then  I can see all the responses are identical for SC802

    Examples:
      | conditions            |
      | client_not_recognised |
      | invalid_bank_account  |
