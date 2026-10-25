@SOAP-API
Feature: Comparison Testing - SC875 - Inquire Medical Appeals Decision

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC875 successful transaction response
    Given I create the correct api payload with different <conditions>
    And   I send the SC875 request to IIB endpoint
    And   I send the SC875 request to Azure endpoint
    Then  I can see all the responses are identical for SC875

    Examples:
      | conditions                               |
      | medical_appeal_status_1372               |
      | medical_appeal_status_1373               |
      | medical_appeal_status_1374               |
      | no_medical_appeal_decision               |
      | client_not_present_in_medical_appeals_db |


  @skip @negative
  Scenario Outline: Compare SC875 unsuccessful transaction response
    Given I create the correct api payload with different <conditions>
    And   I send the SC875 request to IIB endpoint
    And   I send the SC875 request to Azure endpoint
    Then  I can see all the responses are identical for SC875

    Examples:
      | conditions      |
      | invalid_request |
