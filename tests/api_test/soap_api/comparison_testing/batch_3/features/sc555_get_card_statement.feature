@SOAP-API
Feature: Comparison Testing - SC555 - Get Card Statement

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC555 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC555 successful transaction response
    Given I create the correct SC555 api payload with different <conditions>
    And   I send the SC555 request to IIB endpoint
    And   I send the SC555 request to Azure endpoint
    Then  I can see all the responses are identical for SC555

    Examples:
      | conditions         |
      | transactions_found |


  @negative
  Scenario Outline: Compare SC555 unsuccessful transaction responses
    Given I create the correct SC555 api payload with different <conditions>
    And   I send the SC555 request to IIB endpoint
    And   I send the SC555 request to Azure endpoint
    Then  I can see all the responses are identical for SC555

    Examples:
      | conditions                 |
      | no_transactions            |
      | end_date_before_start_date |
      #| invalid_xml                 |
      | unknown_card_number         |
