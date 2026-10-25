@SOAP-API @DP901
Feature: Comparison Testing - DP901 - Manage income

As a client
I want to compare the responses from the IIB and Azure
So that I can see whether the responses are identical

Acceptance:
  * The responses from the IIB and Azure endpoints are identical
  * The result codes are:
    * 90100 - Declaration is received successfully by service provider
    * 90120 - Insufficient Data


  @positive
  Scenario Outline: Compare DP901 successful response for income declaration
    Given I create the api payload for <condition>
    And   I send manage income request to IIB endpoint
    And   I send manage income request to Azure endpoint
    Then  I can see the DP901 responses are identical

    Examples:
      | condition                            |
      | successful_new_income_declaration    |
      | successful_update_income_declaration |


  @negative
  Scenario Outline: Compare DP901 response for unrecognised income type code
    Given I create the api payload for <condition>
    And   I send manage income request to IIB endpoint
    And   I send manage income request to Azure endpoint
    Then  I can see the DP901 responses are identical

    Examples:
      | condition                     |
      | unrecognised_income_type_code |
