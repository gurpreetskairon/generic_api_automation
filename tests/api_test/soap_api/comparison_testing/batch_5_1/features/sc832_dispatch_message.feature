@SOAP-API
Feature: Comparison Testing - SC832 - Dispatch Message

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC832 responses are identical

  The user can get the following status:
  * 83200 - Transaction Successful
  * 83201 - Transaction Unsuccessful


  Scenario Outline: Compare SC832 dispatch message responses
    Given I create the SC832 api payload with <conditions>
    And   I send the SC832 request to IIB endpoint
    And   I send the SC832 request to Azure endpoint
    Then  I can see all the responses are identical for SC832

    @positive
    Examples:
      | conditions          |
      | successful_response |

    @negative
    Examples:
      | conditions            |
      | unsuccessful_response |
