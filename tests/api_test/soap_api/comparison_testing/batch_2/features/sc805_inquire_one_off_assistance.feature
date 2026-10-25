@AZURE-SOAP-API @SOAP-API @sc805-comparison
@inquireassistance
Feature: Comparison Testing - SC805 - Inquire assistance

  As a consumer of the SC805 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC805 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC805 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * A successful request returns result code 80500 and message Transaction Successful.
  * A request with no matching assistance payment returns result code 80501 and message No matching record.

  Execution notes:
  * The same payload is sent to IIB and Azure for each comparison scenario.
  * Dynamic request values are generated once and reused for both endpoints.
  * The successful scenario requires a valid client number and matching payment reference.
  * The no_matching_record scenario requires verified client and payment-reference test data that produces no matching record.


  @positive @successful_response
  Scenario: Compare SC805 successful response
    Given I create the correct SC805 api payload
    When  I send SC805 inquire assistance request to IIB endpoint
    And   I send SC805 inquire assistance request to Azure endpoint
    Then  I can see all the responses are identical for SC805


  @negative @no_matching_record
  Scenario: Compare SC805 no matching record response
    Given I create the SC805 api payload for no_matching_record
    When  I send SC805 inquire assistance request to IIB endpoint
    And   I send SC805 inquire assistance request to Azure endpoint
    Then  I can see all the responses are identical for SC805
