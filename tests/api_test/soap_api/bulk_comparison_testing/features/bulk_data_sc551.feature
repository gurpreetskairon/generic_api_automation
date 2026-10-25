Feature: Comparison Testing - bulk client data (SC551)

  As I have thousands of client data
  I want to send the requests to each Service Contract in batch 1 to IIB and Azure endpoint
  So that I verify the responses from different endpoints are identical

  Acceptance:
  * All the responses from different Service Contract in batch 1 are identical


  Scenario: Verify bulk client data for SC551
    Given I have updated payloads with the bulk data for SC551
    When  I send the request of SC551 to IIB endpoint
    And   I send the request of SC551 to Azure endpoint
    Then  I can see all the responses are identical for SC551
