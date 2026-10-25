@SC575 @COMPARISON @IIB-AZURE @soap-api
Feature: Comparison Testing - SC575 - Match client details using IRD identifier

  As a consumer
  I want to compare SC575 responses between IIB and Azure
  So that I can confirm Azure returns the same SOAP response as IIB for the agreed scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC575 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * Detailed field-level validation is covered under Azure integration testing.

  Notes:
  * The same SC575 payload is sent to both IIB and Azure for each comparison scenario.
  * SC575 matching is based on IRD, name, date of birth and address details.
  * 57504 Too Many Requests is parked for now and will be covered later during full regression testing.
  * 57599 APIM/APIC authentication-related scenario is not included in current SOAP comparison automation. Scope is to compare SOAP responses only.


  @PositiveAC01 @positive @match
  Scenario: Compare SC575 successful Match response
    Given I create an SC575 payload with valid IRD, name, date of birth and address
    When  I send SC575 request to IIB endpoint
    And   I send SC575 request to Azure endpoint
    Then  I can see all the responses are identical for SC575


  @PositiveAC02 @positive @no-match
  Scenario Outline: Compare SC575 No match response
    Given I create an SC575 payload with a valid IRD
    And   I update the payload with a non-matching "<field>"
    When  I send SC575 request to IIB endpoint
    And   I send SC575 request to Azure endpoint
    Then  I can see all the responses are identical for SC575

    Examples:
      | field       |
      | name        |
      | dateOfBirth |


  @NegativeAC01 @negative @transaction-id
  Scenario Outline: Compare SC575 transactionId validation response
    Given I create an SC575 payload with "<transaction_id_condition>"
    When  I send SC575 request to IIB endpoint
    And   I send SC575 request to Azure endpoint
    Then  I can see all the responses are identical for SC575

    Examples:
      | transaction_id_condition     |
      | invalid transactionId format |
      | blank transactionId          |


  @NegativeAC02 @negative @request-validation
  Scenario Outline: Compare SC575 request parameter validation response
    Given I create an SC575 payload with invalid or missing "<field>" using "<condition>"
    When  I send SC575 request to IIB endpoint
    And   I send SC575 request to Azure endpoint
    Then  I can see all the responses are identical for SC575

    Examples:
      | field   | condition                 |
      | IRD     | number less than 9 digits |
      | IRD     | number more than 9 digits |
      | IRD     | blank value               |
      | name    | blank value               |
      | address | blank value               |


  @NegativeAC03 @negative @ird @business-validation
  Scenario: Compare SC575 invalid IRD validation response
    Given I create an SC575 payload with a 9 digit IRD number that is not valid or does not match the customer type
    When  I send SC575 request to IIB endpoint
    And   I send SC575 request to Azure endpoint
    Then  I can see all the responses are identical for SC575
