@AZURE-REST-API @REST-API @dp887-comparison
Feature: Comparison Testing - DP887 - Inquire Ongoing Application

  As a client
  I want to send DP887 inquire ongoing application requests to the DataPower and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the DataPower and Azure endpoints are identical
    * The expected result code and message are:
      * 88700 - Transaction Successful
    * The expected sub-result codes and messages are:
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
    * Invalid request - A schema validation error has occurred while parsing the XML document


  @positive @dp887-positive
  Scenario Outline: Compare DP887 successful response between DataPower and Azure
    Given I create the DP887 api request for <condition>
    When I send DP887 request to DataPower endpoint
    And I send DP887 request to Azure endpoint
    Then I can see all the responses are identical for DP887

    Examples:
      | condition                 |
      | ongoing_application_found |


  @positive @dp887-sub-results
  Scenario Outline: Compare DP887 successful sub-result responses between DataPower and Azure
    Given I create the DP887 api request for <condition>
    When I send DP887 request to DataPower endpoint
    And I send DP887 request to Azure endpoint
    Then I can see all the responses are identical for DP887

    Examples:
      | condition                         |
      | no_primary_application_obligation |
#      | no_partner_application_obligation |
      | no_partner_in_application         |
      | no_primary_supporting_document    |
#      | no_partner_supporting_document    |
      | no_primary_document_evidence      |
      | no_partner_document_evidence      |
      | no_primary_work_obligation        |
      | no_partner_work_obligation        |
      | no_primary_pre_benefit_activity   |
#      | no_partner_pre_benefit_activity   |
      | no_primary_appointments           |


  @negative @dp887-negative
  Scenario Outline: Compare DP887 unsuccessful responses between DataPower and Azure
    Given I create the DP887 api request for <condition>
    When I send DP887 request to DataPower endpoint
    And I send DP887 request to Azure endpoint
    Then I can see all the responses are identical for DP887

    Examples:
      | condition       |
      | invalid_request |
