@AZURE-SOAP-API @SOAP-API @sc836-comparison
Feature: Comparison Testing - SC836 - Notify Document Stored

  As a client,
  I want to send SC836 Notify Document Stored requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 71000 - Transaction successful
      * 71010 - A document is already registered with this document reference id
      * 71020 - Missing mandatory data
      * 71030 - Invalid data
      * 71040 - User account is unknown or not enabled
      * 79999 - Unexpected system error

  Execution Note:
    * Result code 79999 represents an unexpected infrastructure/system error
      and is not included as a runnable comparison scenario.


  @positive @sc836-positive
  Scenario Outline: Compare SC836 successful responses between IIB and Azure
    Given I create the SC836 api payload for <condition>
    When I send SC836 request to IIB endpoint
    And I send SC836 request to Azure endpoint
    Then I can see all the responses are identical for SC836

    Examples:
      | condition           |
      | successful_response |


  @negative @sc836-negative
  Scenario Outline: Compare SC836 unsuccessful responses between IIB and Azure
    Given I create the SC836 api payload for <condition>
    When I send SC836 request to IIB endpoint
    And I send SC836 request to Azure endpoint
    Then I can see all the responses are identical for SC836

    Examples:
      | condition                    |
      | duplicate_document_reference |
      | missing_mandatory_data       |
      | invalid_data                 |
      | user_not_recognised          |
