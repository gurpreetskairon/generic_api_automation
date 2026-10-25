@SOAP-API
Feature: Comparison Testing - SC846 - Advise Sanction

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC846 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @skip @positive
  Scenario Outline: Compare SC846 successful transaction response
    Given I create the correct SC846 api payload with different <conditions>
    And   I send the SC846 request to IIB endpoint
    And   I send the SC846 request to Azure endpoint
    Then  I can see all the responses are identical for SC846

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC846 unsuccessful transaction response
    Given I create the correct SC846 api payload with different <conditions>
    And   I send the SC846 request to IIB endpoint
    And   I send the SC846 request to Azure endpoint
    Then  I can see all the responses are identical for SC846

    Examples:
      | conditions                         |
      | unsuccessful_transaction           |
      | obligation_failure_id_not_supplied |
      | invalid_request                    |
      | client_not_recognised              |
