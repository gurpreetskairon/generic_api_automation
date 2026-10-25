@AZURE-SOAP-API @SOAP-API @sc851-comparison
Feature: Comparison Testing - SC851 - Inquire Case Management Input
  As a client,
  I want to send SC851 Inquire Case Management Input requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical

    * SC851:
      * 85100 - Transaction Successful
      * 85110 - Invalid data

    * Supplementary result codes:
      * 12702 - Traffic Light Status Colour
      * 12703 - Notice Period Start Date
      * 12704 - Notice Period End Date
      * 12705 - NFS Apply Date
      * 12706 - Obligation Failure Status

    * SC127 - Obligation Failure:
      * 12700 - Transaction Successful
      * 12701 - No Obligation Failure Found
      * 12799 - Technical failure

    * SC861 - Appointments and Seminars:
      * 86100 - Appointment(s) found
      * 86101 - No appointments or seminars found
      * 86199 - Technical failure

    * SC804 - Financial Assistance:
      * 80400 - Transaction Successful
      * 80403 - No matching record
      * 80402 - Client not recognised
      * 80499 - Technical failure

    * SC897 - User Activity:
      * 89700 - Transaction Successful
      * 89701 - No matching record
      * 89799 - Technical failure

  Execution Note:
    * A dedicated client with an obligation failure is included to cover the
      Traffic Light System supplementary results 12702, 12703, 12704, 12705
      and 12706.
    * Invalid-format client numbers containing letters or special characters
      return schema validation errors and are not included as business scenarios.
    * A valid-format non-existent client returns SC851 result 85100 with
      downstream results including 86120 and 80402.
    * Missing the entire clientNumber element returns HTTP 500 SOAP Fault
      with SC851 result 85110 - Invalid data.
    * Result codes 86120 and 12707 have been observed at runtime but are not
      listed in the current acceptance criteria.

  @positive @sc851-positive
  Scenario Outline: Compare SC851 successful responses between IIB and Azure
    Given I create the SC851 api payload for <condition>
    When I send SC851 request to IIB endpoint
    And I send SC851 request to Azure endpoint
    Then I can see all the responses are identical for SC851

    Examples:
      | condition                        |
      | successful_response              |
      | traffic_light_obligation_failure |
      | no_matching_downstream_records   |
      | non_existent_client_number       |

  @negative @sc851-negative
  Scenario Outline: Compare SC851 invalid data responses between IIB and Azure
    Given I create the SC851 api payload for <condition>
    When I send SC851 request to IIB endpoint
    And I send SC851 request to Azure endpoint
    Then I can see all the responses are identical for SC851

    Examples:
      | condition             |
      | missing_client_number |
