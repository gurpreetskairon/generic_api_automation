@SOAP-API
Feature: Comparison Testing - SC850 - Create Task

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC850 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC850 successful transaction response
    Given I create the correct SC850 api payload with different <conditions>
    And   I send the SC850 request to IIB endpoint
    And   I send the SC850 request to Azure endpoint
    Then  I can see all the responses are identical for SC850

    Examples:
      | conditions             |
      | successful_transaction |
