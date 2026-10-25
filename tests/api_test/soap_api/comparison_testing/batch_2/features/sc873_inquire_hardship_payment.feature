@AZURE-SOAP-API @SOAP-API @sc873-comparison
@inquirehardshippayment
Feature: Comparison Testing - SC873 - Inquire hardship payment

  As a consumer of the SC873 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC873 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for all covered SC873 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * Detailed result-code and message validation is covered under Azure integration testing.
  * The following client and request conditions are covered:
    * Normal, duplicate, locked, fraudulent and deceased clients with hardship payment records.
    * Client with no hardship payment recorded.
    * Secured client.
    * Client without a current partner when partner hardship payments are requested.
    * Client with a partner who has no hardship payment within the requested period.
    * Unrecognised user or source system.
    * Unrecognised client number.
    * Invalid client-number format.
    * Invalid start-date or end-date format.
    * Request missing the minimum mandatory data.
    * Client and partner with hardship payments when partner inclusion is set to false.


  Execution notes:
  * The same payload is sent to IIB and Azure for each comparison scenario.
  * Dynamic request values such as auditId, transactionId and requestDateTime are generated once and reused for both endpoints.
  * The transaction ID configured in conftest.py is used in the SC873 request.
  * Partner scenarios use includePartnerHardshipPayment as required by the test condition.
  * The search-period dates are supplied through the SC873 payload setup.
  * Stable and verified client data is required for each condition.


  @positive @successful_response
  Scenario Outline: Compare SC873 successful response for supported client types
    Given I create the correct SC873 api payload for <client_type>
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873

    Examples:
      | client_type       |
      | normal_client     |
      | duplicate_client  |
      | locked_client     |
      | fraudulent_client |
      | deceased_client   |


  @positive @no_matching_record
  Scenario: Compare SC873 response when no hardship payment is recorded
    Given I create the SC873 api payload for no_hardship_payment
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873


  @negative @secured_client
  Scenario: Compare SC873 response for a secured client
    Given I create the SC873 api payload for secured_client
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873


  @positive @include_partner @no_partner
  Scenario: Compare SC873 response when the client does not have a partner
    Given I create the SC873 api payload for client_without_partner
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873


  @positive @include_partner @partner_no_matching_record
  Scenario: Compare SC873 response when the partner has no hardship payment
    Given I create the SC873 api payload for partner_without_hardship_payment
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873


  @negative @security
  Scenario: Compare SC873 response for an unrecognised user or source system
    Given I create the SC873 api payload for unrecognised_user
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873


  @negative @client_not_recognised
  Scenario: Compare SC873 response for an unrecognised client
    Given I create the SC873 api payload for unrecognised_client
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873


  @negative @schema_validation
  Scenario Outline: Compare SC873 schema-validation responses
    Given I create the SC873 api payload for <condition>
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873

    Examples:
      | condition             |
      | invalid_client_number |
      | invalid_start_date    |
      | invalid_end_date      |


  @negative @invalid_request
  Scenario: Compare SC873 response when minimum request data is missing
    Given I create the SC873 api payload for missing_minimum_data
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873


  @negative @partner_not_included
  Scenario: Compare SC873 response when partner hardship payment is not requested
    Given I create the SC873 api payload for include_partner_false
    When  I send SC873 inquire hardship payment request to IIB endpoint
    And   I send SC873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for SC873
