@AZURE-SOAP-API @SOAP-API @sc887-comparison
Feature: Comparison Testing - SC887 - Inquire Ongoing Application

  As a client
  I want to send SC887 inquire ongoing application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 88700 - Transaction Successful
      * 88709 - User not recognised
      * 88710 - Invalid Request
    * A successful 88700 response may include the following sub-result codes:
      * 887001 - No application obligation for the primary applicant
      * 887002 - No application obligation for the partner
      * 887003 - No partner included in the application
      * 887004 - No supporting document required for the primary applicant
      * 887005 - No supporting document required for the partner
      * 887006 - No application document evidence exists for primary
      * 887007 - No application document evidence exists for partner
      * 887008 - No work obligation available for primary
      * 887009 - No work obligation available for partner
      * 887010 - No pre-benefit activity available for primary
      * 887011 - No pre-benefit activity available for partner
      * 887012 - No appointments available for primary


  @positive @sc887-positive
  Scenario Outline: Compare SC887 successful responses between IIB and Azure
    Given I create the SC887 api payload for <condition>
    When  I send SC887 request to IIB endpoint
    And   I send SC887 request to Azure endpoint
    Then  I can see all the responses are identical for SC887

    Examples:
      | condition                 |
      | ongoing_application_found |

  @positive @subresult @sc887-subresult
  Scenario Outline: Compare SC887 successful sub-result responses between IIB and Azure
    Given I create the SC887 api payload for <condition>
    When I send SC887 request to IIB endpoint
    And I send SC887 request to Azure endpoint
    Then I can see all the responses are identical for SC887

    Examples:
      | condition                           |
      | no_primary_application_obligation   |
#      | no_partner_application_obligation   |
      | no_partner_in_application           |
      | no_primary_supporting_document      |
#      | no_partner_supporting_document      |
      | no_primary_document_evidence        |
      | no_partner_document_evidence        |
      | no_primary_work_obligation          |
      | no_partner_work_obligation          |
      | no_primary_pre_benefit_activity     |
#      | no_partner_pre_benefit_activity     |
      | no_primary_appointments             |


  @negative @sc887-negative
  Scenario Outline: Compare SC887 unsuccessful responses between IIB and Azure
    Given I create the SC887 api payload for <condition>
    When  I send SC887 request to IIB endpoint
    And   I send SC887 request to Azure endpoint
    Then  I can see all the responses are identical for SC887

    Examples:
      | condition           |
      | no_matching_record  |
      | user_not_recognised |
      | invalid_request     |
