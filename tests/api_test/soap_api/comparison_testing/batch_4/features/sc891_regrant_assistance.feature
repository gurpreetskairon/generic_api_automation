@AZURE-SOAP-API @SOAP-API @sc891-comparison
Feature: Comparison Testing - SC891 - ReGrant Assistance

  As a client
  I want to send SC891 ReGrant Assistance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 89100 - Transaction Successful - No further action
      * 89102 - Transaction Successful - Further action required
      * 89101 - Transaction Unsuccessful
      * 89103 - Unsuccessful - Assistance not re-granted
      * 80099 - Result Not Recognised

  Execution Note:
    * The 80099 Result Not Recognised scenario requires an unrecognised provider result and will only be automated when suitable test data or a reliable trigger is identified.


  @positive @sc891-positive
  Scenario Outline: Compare SC891 successful responses between IIB and Azure
    Given I create the SC891 api payload for <condition>
    When  I send SC891 request to IIB endpoint
    And   I send SC891 request to Azure endpoint
    Then  I can see all the responses are identical for SC891

    Examples:
      | condition               |
      | no_further_action       |
      | further_action_required |


  @negative @sc891-negative
  Scenario Outline: Compare SC891 unsuccessful responses between IIB and Azure
    Given I create the SC891 api payload for <condition>
    When  I send SC891 request to IIB endpoint
    And   I send SC891 request to Azure endpoint
    Then  I can see all the responses are identical for SC891

    Examples:
      | condition                |
      | transaction_unsuccessful |
      | assistance_not_regranted |
