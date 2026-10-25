@AZURE-SOAP-API @SOAP-API @sc828-comparison @manageparticipant
@inquireparticipant
Feature: Comparison Testing - SC828 - Inquire participant

  As a consumer of the SC828 SOAP service
  I want to send the same SC828 SOAP request to IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for SC828 business responses

  Acceptance:
  * Azure and IIB responses should be identical for the agreed SC828 comparison scenarios
  * XML namespace prefixes are not treated as business-data differences
  * Detailed field-level validation is covered under Azure integration testing

  Execution notes:
  * The same SC828 payload is sent to both IIB and Azure for each comparison scenario.
  * SC828 matching is based on client name and date of birth.
  * The expected business conditions and behaviour for locked/duplicate client matching are not confirmed.
  * As agreed with BA, locked/duplicate client behaviour should be covered during functional regression testing.


  @positive @successful_response @response_comparison
  Scenario: Compare SC828 successful response
    Given I created the correct SC828 api payload
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC828


  @positive @matched_client_details @match_confidence @response_comparison
  Scenario Outline: Compare SC828 successful matched client confidence details
    Given I created the correct SC828 api payload for <client_match_condition>
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC828

    Examples:
      | client_match_condition       |
      | full_name_100_dob_100        |
      | full_name_95_dob_100         |
      | full_name_85_dob_100         |
      | full_name_100_dob_day_month  |
      | full_name_100_dob_day_year   |
      | full_name_100_dob_month_year |


  @positive @special_client_records @response_comparison
  Scenario Outline: Compare SC828 matched client details for supported special client record types
    Given I created the correct SC828 api payload for <client_match_condition>
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC828

    Examples:
      | client_match_condition |
      | deceased_client        |
      | fraud_client           |
      | secured_client         |


  @positive @no_matching_record @response_comparison
  Scenario: Compare SC828 no matching record response
    Given I created the correct SC828 api payload for no_matching_client
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC828


  @negative @invalid_request @too_short_name @response_comparison
  Scenario: Compare SC828 invalid request response for too short client name
    Given I created the invalid SC828 api payload for too_short_name
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC828


  @negative @invalid_request @missing_dob @response_comparison
  Scenario: Compare SC828 invalid request response when date of birth is missing from request
    Given I created the invalid SC828 api payload for missing_dob
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC828
