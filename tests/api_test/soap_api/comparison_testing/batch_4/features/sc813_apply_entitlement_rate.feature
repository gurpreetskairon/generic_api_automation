@SOAP-API
Feature: Comparison Testing - SC813 - Apply Entitlement Rate

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC813 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC813 successful transaction response
    Given I create the correct SC813 api payload with different <conditions>
    And   I send the SC813 request to IIB endpoint
    And   I send the SC813 request to Azure endpoint
    Then  I can see all the responses are identical for SC813

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC813 unsuccessful transaction response
    Given I create the correct SC813 api payload with different <conditions>
    And   I send the SC813 request to IIB endpoint
    And   I send the SC813 request to Azure endpoint
    Then  I can see all the responses are identical for SC813

    Examples:
      | conditions            |
      | invalid_request       |
      | client_not_recognised |
      | swiftt_user_not_found |
