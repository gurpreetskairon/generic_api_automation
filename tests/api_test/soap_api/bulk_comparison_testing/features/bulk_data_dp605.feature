Feature: Comparison Testing - bulk client data (DP605)

  As I have thousands of client data
  I want to send the requests to each Service Contract in batch 1 to IIB and Azure endpoint
  So that I verify the responses from different endpoints are identical

  Acceptance:
  * All the responses from different Service Contract in batch 1 are identical


  Scenario: Verify bulk client data for DP605
    Given I have updated payloads with the bulk data for DP605
    And   I used a valid client number as the DP605 path parameter
    When  I send the request of DP605 to IIB endpoint
    And   I send the request of DP605 to Azure endpoint
    Then  I can see all the responses are identical for DP605
