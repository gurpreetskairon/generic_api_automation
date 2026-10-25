@IIB-AZURE-COMPARISON @SOAP-API @DP812-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - DP812 - Inquire entitlement

  As a client
  I want to compare the responses from the IIB and Azure for DP812
  So that I can see whether the responses are identical


Notes:


  @positive
  Scenario Outline: Compare DP812 successful responses with different entitlement factors
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical
    Examples:
    | conditions                  |
    |none                         |
    |INCOMEABATEMENT              |
    |SANCTION                     |
    |SECTION70A                   |
    |TenYearsNZResidencySinceBirth|

  @positive
  Scenario Outline: Compare DP812 successful responses with different optional params
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical
    Examples:
    | conditions                      |
    |includeFullEntitlement_No        |
    |includeNotionalRate_No           |
    |includePaymentRate_No            |
    |includePortabilityProvision_No   |
    |includeTaxRate_No                |

  @negative
  Scenario Outline: Compare DP812 responses for unknown client
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical
    Examples:
    | conditions               |
    | client_not_recognised    |
    | invalid_request          |
    | no_matching_record       |
