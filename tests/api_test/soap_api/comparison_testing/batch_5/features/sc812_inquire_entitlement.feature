@IIB-AZURE-COMPARISON @SOAP-API @sc812-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC812 - Inquire ongoing assistance

  As a client
  I want to compare the responses from the IIB and Azure for SC812
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare SC812 successful response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions           |
      | decades_old_services |
      | js_current           |
      | no_matching_record   |


  @negative
  Scenario Outline: Compare SC812 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical
    Examples:
    | conditions               |
    | client_not_recognised    |

