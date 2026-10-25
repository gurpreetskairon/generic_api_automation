@AZURE-SOAP-API @SOAP-API @sc879-comparison
Feature: Comparison Testing - SC879 - Inquire Hardship Application Summary

  As a client
  I want to send SC879 Inquire Hardship Application Summary requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 87900 - Transaction Successful
      * 87901 - No matching record
      * 87909 - User not recognised
      * 87910 - Invalid Request
      * 87911 - Client not recognised

  Execution Note:
    * The current implementation supports filtering by search period and application status
    * Filtering by needTypeCode and outcome is not supported in the current implementation and these fields should not be populated


  @positive @sc879-positive
  Scenario Outline: Compare SC879 successful responses between IIB and Azure
    Given I create the SC879 api payload for <condition>
    When  I send SC879 request to IIB endpoint
    And   I send SC879 request to Azure endpoint
    Then  I can see all the responses are identical for SC879

    Examples:
      | condition                     |
      | hardship_application_found    |
      | no_hardship_application_found |


  @negative @sc879-negative
  Scenario Outline: Compare SC879 unsuccessful responses between IIB and Azure
    Given I create the SC879 api payload for <condition>
    When  I send SC879 request to IIB endpoint
    And   I send SC879 request to Azure endpoint
    Then  I can see all the responses are identical for SC879

    Examples:
      | condition             |
      | user_not_recognised   |
      | invalid_request       |
      | client_not_recognised |
