@SOAP-API @DP806V2
Feature: Comparison Testing - DP806V2 - Inquire debt

As a client
I want to compare the responses from the IIB and Azure
So that I can see whether the responses are identical

Acceptance:
* The responses from the IIB and Azure endpoints are identical
* The result codes are:
    * 80600 - Transaction Successful
    * 80601 - No Matching Record

Execution Note:
* Scenarios with includeHeritageDebt set to true are currently blocked due to
    WAM/S2P database connectivity not being available in Azure.
* The connectivity dependency is tracked under API-3500.
* Retest the affected scenarios once the connectivity is established.


  @positive
  Scenario Outline: Compare DP806V2 successful response for debt details
    Given I create the api payload for <condition>
    And   I send inquire debt request to IIB endpoint
    And   I send inquire debt request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | condition                               |
      | successful_response_heritage_debt_true  |
      | successful_response_heritage_debt_false |


  @negative
  Scenario Outline: Compare DP806V2 response when no matching debt record exists
    Given I create the api payload for <condition>
    And   I send inquire debt request to IIB endpoint
    And   I send inquire debt request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | condition                                |
      | no_matching_record_heritage_debt_true    |
      | no_matching_record_heritage_debt_false   |
      | invalid_client_number_heritage_debt_true |
