Feature: Comparison Testing - bulk client data (SC829)

  As I have thousands of client data
  I want to send the same SC829 request to both IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
  * IIB and Azure responses are identical for the SC829 bulk comparison scenario

  Note:
  * Detailed validation of result code, status message and client number is covered under Azure integration testing.
  * Bulk comparison testing sends the same SC829 payload to IIB and Azure and validates that both endpoint responses are identical.
  * XML namespace prefixes are not treated as business-data differences.
  * XML element ordering is normalized where IIB and Azure return the same values in a different order.


  Scenario: Verify bulk client data for SC829
    Given I have updated payloads with the bulk data for SC829
    When  I send the request of SC829 to IIB endpoint
    And   I send the request of SC829 to Azure endpoint
    Then  I can see all the responses are identical for SC829
