@AZURE-SOAP-API @SOAP-API @sc856-comparison
Feature: Comparison Testing - SC856 - Inquire Pay Period and Redirections

  As a client
  I want to send SC856 inquire pay period and redirections requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 85600 - Transaction Successful - Pay period and redirections have been successfully returned by SWIFTT
      * 85601 - Transaction Successful - Pay period returned and redirections are not available for the client
      * 85602 - Transaction Unsuccessful - Invalid redirection type
      * 85611 - Client not recognised - Client number does not exist in the source system

  Execution Note:
    * SC856 returns current or future pay period and redirection information for a client.
    * The current scope covers EHC redirections.
    * The acceptance criteria supplied for automation are treated as the source of truth where older
      service documentation contains different or superseded result-code descriptions.


  @positive @sc856-positive
  Scenario Outline: Compare SC856 successful responses between IIB and Azure
    Given I create the SC856 api payload for <condition>
    When  I send SC856 request to IIB endpoint
    And   I send SC856 request to Azure endpoint
    Then  I can see all the responses are identical for SC856

    Examples:
      | condition                       |
      | pay_period_and_redirections     |
      | pay_period_without_redirections |


  @negative @sc856-negative
  Scenario Outline: Compare SC856 unsuccessful responses between IIB and Azure
    Given I create the SC856 api payload for <condition>
    When  I send SC856 request to IIB endpoint
    And   I send SC856 request to Azure endpoint
    Then  I can see all the responses are identical for SC856

    Examples:
      | condition                |
      | invalid_redirection_type |
      | unrecognised_client      |
