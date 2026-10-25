@SOAP-API
Feature: Comparison Testing - SC803 - Change Assistance Status

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC803 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC803 successful transaction response
    Given I create the correct SC803 api payload with different <conditions>
    And   I send the SC803 request to IIB endpoint
    And   I send the SC803 request to Azure endpoint
    Then  I can see all the responses are identical for SC803

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC803 unsuccessful transaction response
    Given I create the correct SC803 api payload with different <conditions>
    And   I send the SC803 request to IIB endpoint
    And   I send the SC803 request to Azure endpoint
    Then  I can see all the responses are identical for SC803

    Examples:
      | conditions               |
      | unsuccessful_transaction |
      | client_not_recognised    |
