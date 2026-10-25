@AZURE-SOAP-API @SOAP-API @sc127-comparison
Feature: Comparison Testing - SC127 - Get Client Obligation Failure

  As a client,
  I want to send SC127 Get Client Obligation Failure requests
  to the IIB and Azure endpoints
  So that I can verify the responses are identical


  @positive
  Scenario Outline: Compare SC127 successful transaction response
    Given I create the SC127 api payload for <condition>
    When I send SC127 request to IIB endpoint
    And I send SC127 request to Azure endpoint
    Then I can see all the responses are identical for SC127

    Examples:
      | condition              |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC127 no obligation failure response
    Given I create the SC127 api payload for <condition>
    When I send SC127 request to IIB endpoint
    And I send SC127 request to Azure endpoint
    Then I can see all the responses are identical for SC127

    Examples:
      | condition             |
      | no_obligation_failure |
