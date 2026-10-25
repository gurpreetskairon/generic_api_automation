@AZURE-SOAP-API @SOAP-API @sc898-comparison
@inquireeligibility
Feature: Comparison Testing - SC898 - Inquire Eligibility

  As a consumer of the SC898 SOAP service
  I want to compare the SC898 response between Azure and IIB
  So that I can confirm Azure behaves like-for-like with IIB for the agreed scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the agreed SC898 comparison scenarios
  * XML namespace prefixes are not treated as business-data differences
  * Detailed field-level validation is covered under Azure integration testing

  Notes:
  * Comparison testing sends the same payload to Azure and IIB and validates that both endpoint responses are identical.
  * no_c2e_flag scenario is excluded from automation because expiryDate behaviour is data-dependent and not part of the current acceptance criteria.
  * Empty correlationId returned by IIB is treated as an agreed technical header difference and is handled by the common SOAP comparison helper.


  @positive @successful_response @click_to_enrol
  Scenario Outline: Compare SC898 successful Click to Enrol eligibility response between Azure and IIB
    Given I created the correct SC898 api payload for <client_flag_condition>
    When  I send the SC898 request to both Azure and IIB endpoints
    Then  I can see all the responses are identical for SC898

    Examples:
      | client_flag_condition |
      | active_c2e_flag       |
      | expired_c2e_flag      |


  @negative @business_response
  Scenario Outline: Compare SC898 negative business response between Azure and IIB
    Given I created the SC898 api payload for <negative_condition>
    When  I send the SC898 request to both Azure and IIB endpoints
    Then  I can see all the responses are identical for SC898

    Examples:
      | negative_condition    |
      | no_matching_client    |
      | invalid_client_number |
      | user_not_recognised   |


  @negative @missing_client_number @exception_response
  Scenario: Compare SC898 missing client number exception response between Azure and IIB
    Given I created the SC898 api payload for missing_client_number
    When  I send the SC898 request to both Azure and IIB endpoints
    Then  I can see all the responses are identical for SC898
