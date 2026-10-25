@SOAP-API
Feature: Comparison Testing - SC876 - Manage Debt and Arrears

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC876 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC876 successful transaction response
    Given I create the correct SC876 api payload with different <conditions>
    And   I send the SC876 request to IIB endpoint
    And   I send the SC876 request to Azure endpoint
    Then  I can see all the responses are identical for SC876

    Examples:
      | conditions         |
      | successful_request |


  @negative
  Scenario Outline: Compare SC876 unsuccessful transaction responses
    Given I create the correct SC876 api payload with different <conditions>
    And   I send the SC876 request to IIB endpoint
    And   I send the SC876 request to Azure endpoint
    Then  I can see all the responses are identical for SC876

    Examples:
      | conditions            |
      | invalid_message       |
      | unrecognised_cnp_id   |
      | swiftt_user_not_found |
