@AZURE-SOAP-API @SOAP-API @sc889-comparison
Feature: Comparison Testing - SC889 - Verify Assistance

  As a client
  I want to send SC889 Verify Assistance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes defined in the requirements are:
      * 88900 - Transaction Successful
      * 88902 - Error - Assistance not verified
      * 88903 - Not a valid income type
      * 88904 - Income limit exceeded
      * 80099 - Result Not Recognised

  Execution Note:
    * Current IIB testing can reliably reproduce 88900 and 88902 responses.
    * Invalid income type does not currently reproduce 88903. An invalid income type still returns 88900.
    * Excess income does not currently reproduce 88904 as the top-level result. IIB returns 88902 with provider sub-results explaining the income-related failure.
    * 80099 cannot currently be reproduced because no reliable trigger or suitable test data has been identified.
    * Additional 88902 scenarios are covered using provider validation failures such as invalid bank type, invalid entitlement code, and incorrect application date / Date of First Contact.


  @positive @sc889-positive
  Scenario Outline: Compare SC889 successful responses between IIB and Azure
    Given I create the SC889 api payload for <condition>
    When  I send SC889 request to IIB endpoint
    And   I send SC889 request to Azure endpoint
    Then  I can see all the responses are identical for SC889

    Examples:
      | condition           |
      | successful_response |


  @negative @sc889-negative
  Scenario Outline: Compare SC889 assistance verification failures between IIB and Azure
    Given I create the SC889 api payload for <condition>
    When  I send SC889 request to IIB endpoint
    And   I send SC889 request to Azure endpoint
    Then  I can see all the responses are identical for SC889

    Examples:
      | condition                  |
      | income_limit_exceeded      |
      | invalid_bank_type          |
      | invalid_entitlement_code   |
      | incorrect_application_date |
