@AZURE-SOAP-API @SOAP-API @sc814-comparison
Feature: Comparison Testing - SC814 - Inquire Exchange Rate

  As a client
  I want to send SC814 inquire exchange rate requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 81400 - Transaction Successful
      * 81402 - Nothing held for this request
      * 81401 - Invalid Request
      * 80099 - Result Not Recognised

  Execution Note:
    * Result code 81402 is not covered by automation because no suitable D11 test data or known request
      combination has been identified to return Nothing held for this request.
    * Result code 81401 is covered using an invalid date range where the end date is earlier than the start date.
    * Invalid paycycle values result in request/schema validation rather than business result code 81401 and are
      therefore not used for this acceptance scenario.
    * Result code 80099 is SWIFTT dependent and cannot currently be reliably triggered through automation.


  @positive @sc814-positive
  Scenario Outline: Compare SC814 successful responses between IIB and Azure
    Given I create the SC814 api payload for <condition>
    When  I send SC814 request to IIB endpoint
    And   I send SC814 request to Azure endpoint
    Then  I can see all the responses are identical for SC814

    Examples:
      | condition             |
      | successful_paycycle_0 |
      | successful_paycycle_1 |
      | successful_paycycle_2 |
      | successful_paycycle_3 |
      | successful_paycycle_4 |
      | successful_paycycle_5 |


  @negative @sc814-negative
  Scenario: Compare SC814 invalid request response between IIB and Azure
    Given I create the SC814 api payload for invalid_date_range
    When  I send SC814 request to IIB endpoint
    And   I send SC814 request to Azure endpoint
    Then  I can see all the responses are identical for SC814


  @negative @sc814-negative
  Scenario: Compare SC814 response for an invalid country code between IIB and Azure
    Given I create the SC814 api payload for invalid_country_code
    When  I send SC814 request to IIB endpoint
    And   I send SC814 request to Azure endpoint
    Then  I can see all the responses are identical for SC814
