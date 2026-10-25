@AZURE-SOAP-API @SOAP-API @sc875-integration
Feature: Integration Testing - SC875 - Inquire Medical Appeals Decision

  As a client
  I want to send SOAP requests to the Azure API
  So that I can validate the response returned for medical appeal decisions


  @positive
  Scenario Outline: Check SC875 successful transaction response
    Given I create the correct payload for <conditions>
    And   I send the request to the Azure SC875 endpoint
    Then  I can see result code <result_code> returned
    And   I can see result message "<result_message>" returned
    And   I can see hasMedicalAppealDecision "<has_medical_appeal_decision>" returned

    Examples:
      | conditions                               | result_code | result_message         | has_medical_appeal_decision |
      | medical_appeal_status_1372               | 87500       | Transaction Successful | true                        |
      | medical_appeal_status_1373               | 87500       | Transaction Successful | true                        |
      | medical_appeal_status_1374               | 87500       | Transaction Successful | true                        |
      | no_medical_appeal_decision               | 87500       | Transaction Successful | false                       |
      | client_not_present_in_medical_appeals_db | 87500       | Transaction Successful | false                       |


  @skip @negative
  Scenario Outline: Check SC875 unsuccessful transaction response
    Given I create the payload with <conditions>
    And   I send the request to the Azure SC875 endpoint
    Then  I can see result code <result_code> returned
    And   I can see result message "<result_message>" returned

    Examples:
      | conditions      | result_code | result_message           |
      | invalid_request | 87501       | Transaction Unsuccessful |
