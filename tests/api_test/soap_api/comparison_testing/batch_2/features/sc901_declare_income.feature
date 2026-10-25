@AZURE-SOAP-API @SOAP-API @sc901-comparison
@manageincome @declareincome
Feature: Comparison Testing - SC901 - Declare income

  As a consumer of the SC901 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC901 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC901 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * A successful new income declaration returns result code 90100 and message Declaration is received successfully by service provider. Further manual processing may or may not be required.
  * A successful update to an existing income declaration returns result code 90100 and message Declaration is received successfully by service provider. Further manual processing may or may not be required.
  * A request containing an unrecognised income master-data type returns result code 90120 and message Insufficient Data. Please verify that the request complies with the service contract - SC901.

  Execution notes:
  * The same payload is sent to both IIB and Azure for each comparison scenario.
  * Each request contains an income declaration for one client and one assessment period.
  * The action is set to NEW for a new declaration and UPDATE for an existing declaration.
  * An income declaration may contain multiple income entries.
  * Income and childcare cost sections are populated only when available.
  * Income and childcare cost frequencies currently support weekly frequency only.
  * No business validation is performed on the client number; only schema validation is applied to the request payload.


  @positive
  Scenario Outline: Compare SC901 successful declare income responses
    Given I create the SC901 api payload for <condition>
    When  I send SC901 declare income request to IIB endpoint
    And   I send SC901 declare income request to Azure endpoint
    Then  I can see all the responses are identical for SC901

    Examples:
      | condition                            |
      | successful_new_income_declaration    |
      | successful_update_income_declaration |


  @negative
  Scenario Outline: Compare SC901 responses for unrecognised income master data
    Given I create the SC901 api payload for <condition>
    When  I send SC901 declare income request to IIB endpoint
    And   I send SC901 declare income request to Azure endpoint
    Then  I can see all the responses are identical for SC901

    Examples:
      | condition                     |
      | unrecognised_income_type_code |
