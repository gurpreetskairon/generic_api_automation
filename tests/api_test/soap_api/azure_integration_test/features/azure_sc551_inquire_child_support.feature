@SOAP-API @inquirechildsupport
Feature: Azure Integration - SC551 - inquire child support service

  As a client
  I want to verify the responses from the Azure
  So that I can see whether the responses are we expected

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Verify SC551 successful response
    Given I create the correct api payload
    And   I send the child support request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see the responses are identical

    Examples:
      | result_code |
      | 55100       |


  @negative
  Scenario Outline: Verify SC551 responses when the request details contain invalid values
    Given I create the api payload with different <conditions>
    And   I send the child support request to Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see subresult message <subresult_message> is the same in both responses

    Examples:
      | conditions                     | result_code | subresult_message                                           |
      | invalid start month            | 55101       | The request parameters are invalid.                         |
      | invalid ird number             | 55102       | IRD number failed check digit.                              |
      | missing ird number             | 55103       | IRD number not found.                                       |
      | inactive liable parent account | 55104       | The customer does not have an active liable parent account. |
      | invalid date range             | 55107       | Date range must be less than one year.                      |
      | invalid start date             | 55108       | Start month must be on or after July-2023.                  |
