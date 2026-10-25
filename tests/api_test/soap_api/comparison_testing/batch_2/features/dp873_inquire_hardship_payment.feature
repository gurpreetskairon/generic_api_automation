@AZURE-SOAP-API @SOAP-API @DP873-comparison
@inquirehardshippayment
Feature: Comparison Testing - DP873 - Inquire hardship payment

  As a consumer of the DP873 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed DP873 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for all covered DP873 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.


  @positive @successful_response
  Scenario Outline: Compare DP873 successful response for supported client types
    Given I create the correct dp873 api payload for <client_type>
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873

    Examples:
      | client_type       |
      | normal_client     |
      | duplicate_client  |
      | locked_client     |
      | fraudulent_client |
      | deceased_client   |


  @positive
  Scenario: Compare DP873 response when no hardship payment is recorded
    Given I create the dp873 api payload for no_hardship_payment
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873


  @negative
  Scenario: Compare DP873 response for a secured client
    Given I create the dp873 api payload for secured_client
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873


  @positive @include_partner @no_partner
  Scenario: Compare DP873 response when the client does not have a partner
    Given I create the dp873 api payload for client_without_partner
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873


  @positive @include_partner @partner_no_matching_record
  Scenario: Compare DP873 response when the partner has no hardship payment
    Given I create the dp873 api payload for partner_without_hardship_payment
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873


  @negative @security
  Scenario: Compare DP873 response for an unrecognised user or source system
    Given I create the dp873 api payload for unrecognised_user
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873


  @negative @client_not_recognised
  Scenario: Compare DP873 response for an unrecognised client
    Given I create the dp873 api payload for unrecognised_client
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873


  @negative @schema_validation
  Scenario Outline: Compare DP873 schema-validation responses
    Given I create the dp873 api payload for <condition>
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873

    Examples:
      | condition             |
      | invalid_client_number |


  @negative @invalid_request
  Scenario: Compare DP873 response when minimum request data is missing
    Given I create the dp873 api payload for missing_minimum_data
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873


  @negative @partner_not_included
  Scenario: Compare DP873 response when partner hardship payment is not requested
    Given I create the dp873 api payload for include_partner_false
    When  I send dp873 inquire hardship payment request to IIB endpoint
    And   I send dp873 inquire hardship payment request to Azure endpoint
    Then  I can see all the responses are identical for dp873
