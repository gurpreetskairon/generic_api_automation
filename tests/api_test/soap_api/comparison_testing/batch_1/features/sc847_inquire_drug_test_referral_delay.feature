@AZURE-SOAP-API @IIB-SOAP-API @SOAP-API @comparison-testing
@sc847-comparison @inquiredrugtestreferraldelay
Feature: Comparison Testing - SC847 - Inquire Drug Test Referral Delay

  As a consumer of the SC847 SOAP service
  I want to compare the SC847 response between Azure and IIB
  So that I can confirm Azure behaves like-for-like with IIB for the agreed scenarios

  Acceptance:
  * Azure and IIB responses are identical for the same SC847 request payload
  * XML namespace prefixes are not treated as business-data differences
  * Detailed field-level validation is covered under Azure integration testing


  @positive @successful_response @drug_test_referral_delay
  Scenario Outline: Compare SC847 successful Drug Test Referral Delay response between Azure and IIB
    Given I created the correct SC847 api payload for <dtrd_condition>
    When  I send the SC847 request to both Azure and IIB endpoints
    Then  I can see all the responses are identical for SC847

    Examples:
      | dtrd_condition                      |
      | dtrd_prescription_medication        |
      | dtrd_receiving_treatment            |
      | dtrd_awaiting_treatment             |
      | dtrd_diagnosed_dependence           |
      | dtrd_drug_help_required             |
      | dtrd_drug_other                     |
      | dtrd_drug_no_good_sufficient_reason |
      | dtrd_drug_brief_interventions       |
      | dtrd_drug_referred_assessment       |


  @positive @no_matching_record
  Scenario Outline: Compare SC847 no matching record response between Azure and IIB
    Given I created the correct SC847 api payload for <dtrd_condition>
    When  I send the SC847 request to both Azure and IIB endpoints
    Then  I can see all the responses are identical for SC847

    Examples:
      | dtrd_condition |
      | no_active_dtrd |
