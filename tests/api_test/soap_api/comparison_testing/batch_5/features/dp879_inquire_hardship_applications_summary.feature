@AZURE-REST-API @REST-API @dp879-comparison
Feature: Comparison Testing - DP879 - Inquire Hardship Applications Summary

  As a client
  I want to send DP879 Inquire Hardship Applications Summary requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result codes are:
      * 87900 - Transaction Successful
      * 87901 - No matching record
      * 87909 - User not recognised
      * 87910 - Invalid Request
      * 87911 - Client not recognised

  Execution Note:
    * The request supports filtering by search period and application status
    * The REST query parameters include transactionId, clientNumber, searchPeriodStart, searchPeriodEnd, and status
    * Filtering by needTypeCode and outcome is not included in the DP879 REST request

  @positive @dp879-positive
  Scenario Outline: Compare DP879 successful responses between DataPower and Azure
    Given I create the DP879 api request for <condition>
    When I send DP879 request to DataPower endpoint
    And I send DP879 request to Azure endpoint
    Then I can see all the responses are identical for DP879

    Examples:
      | condition                              |
      | hardship_application_found             |
      | hardship_application_found_with_filters |
      | no_hardship_application_found          |

  @negative @dp879-negative
  Scenario Outline: Compare DP879 unsuccessful responses between DataPower and Azure
    Given I create the DP879 api request for <condition>
    When I send DP879 request to DataPower endpoint
    And I send DP879 request to Azure endpoint
    Then I can see all the responses are identical for DP879

    Examples:
      | condition             |
      | user_not_recognised   |
      | invalid_request       |
      | client_not_recognised |
