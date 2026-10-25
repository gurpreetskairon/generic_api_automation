@AZURE-SOAP-API @SOAP-API @SC806v2-comparison
@inquiredebt
Feature: Comparison Testing - SC806V2 - Inquire debt

  As a consumer of the SC806v2 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC806v2 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC806v2 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * A successful response returns result code 80600 and message Transaction Successful.
  * A request where no matching debt exists returns result code 80601 and message No Matching Record.

  Execution notes:
  * The same payload is sent to both IIB and Azure for each comparison scenario.
  * Dynamic request values such as auditId, correlationId, transactionId and requestDateTime are generated once and reused for both endpoints.
  * The successful-response client must have one or more debt or debt-repayment records.
  * The no-matching-record client must not have debt matching the requested filter criteria.


  @positive @successful_response
  Scenario: Compare SC806v2 successful response
    Given I create the correct SC806v2 api payload
    When  I send SC806v2 inquire debt request to IIB endpoint
    And   I send SC806v2 inquire debt request to Azure endpoint
    Then  I can see all the responses are identical for SC806v2


  @negative @no_matching_record
  Scenario: Compare SC806v2 no matching record response
    Given I create the SC806v2 api payload for no_matching_record
    When  I send SC806v2 inquire debt request to IIB endpoint
    And   I send SC806v2 inquire debt request to Azure endpoint
    Then  I can see all the responses are identical for SC806v2
