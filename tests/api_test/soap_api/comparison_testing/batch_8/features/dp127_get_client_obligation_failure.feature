@AZURE-REST-API @REST-API @dp127-comparison
Feature: Comparison Testing - DP127 - Get Client Obligation Failure

  As a client,
  I want to send DP127 GET requests to IIB and Azure endpoints
  So that I can verify the responses are identical

  @positive
  Scenario Outline: Compare DP127 successful transaction response
    Given I create the DP127 api request for <condition>
    When I send DP127 request to IIB endpoint
    And I send DP127 request to Azure endpoint
    Then I can see all the responses are identical for DP127

    Examples:
      | condition              |
      | successful_transaction |

  @negative
  Scenario Outline: Compare DP127 no obligation failure response
    Given I create the DP127 api request for <condition>
    When I send DP127 request to IIB endpoint
    And I send DP127 request to Azure endpoint
    Then I can see all the responses are identical for DP127

    Examples:
      | condition             |
      | no_obligation_failure |
