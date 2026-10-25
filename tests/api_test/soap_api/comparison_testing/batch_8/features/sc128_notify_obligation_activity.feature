
@AZURE-SOAP-API @SOAP-API @sc128-comparison
Feature: Comparison Testing - SC128 - Advise Obligation Activity

  As a client,
  I want to send SC128 Advise Obligation Activity requests
  to the IIB and Azure endpoints
  So that I can verify the responses are identical

  @positive
  Scenario Outline: Compare SC128 successful transaction response
    Given I create the SC128 api payload for <condition>
    When I send SC128 request to IIB endpoint
    And I send SC128 request to Azure endpoint
    Then I can see all the responses are identical for SC128

    Examples:
      | condition              |
      | successful_transaction |

  @negative
  Scenario Outline: Compare SC128 existing obligation failure response
    Given I create the SC128 api payload for <condition>
    When I send SC128 request to IIB endpoint
    And I send SC128 request to Azure endpoint
    Then I can see all the responses are identical for SC128

    Examples:
      | condition                   |
      | existing_obligation_failure |
