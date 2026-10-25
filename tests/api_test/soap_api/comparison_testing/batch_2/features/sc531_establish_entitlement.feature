@SOAP-API @SC531
Feature: Comparison Testing - SC531 - Establish Entitlement

As a client
I want to send SC531 establish entitlement requests to the IIB and Azure endpoints
So that I can verify the responses from both endpoints are identical

Acceptance:
  * The responses from the IIB and Azure endpoints are identical
  * The expected result codes are:
    * 52011 - The 52 week reapplication was successfully completed and the result has been recorded in SWIFTT
    * 52012 - The 52 week reapplication has not been successful
    * 52013 - A letter to advise the client their JSS benefit has been re-granted will be sent by SWIFTT overnight
    * 52014 - The client must successfully reapply or their benefit will be suspended from the anniversary date
    * 52015 - The benefit is suspended or expired and must be resumed manually
    * 52002 - User identifier not recognised
    * 52003 - Client not recognised
    * 52005 - The client is not eligible or not required to be reassessed at this time

Execution Note:
  * Successful JSS reapplication scenarios require a client with a pending 52 week reapplication
    that is currently within the valid reapplication period.
  * Once a successful reapplication has been processed, the same client may no longer have a
    pending reassessment. Re-running the request for that client may therefore return 52005.
  * Test data for successful scenarios must be refreshed or replaced when the pending
    52 week reapplication has already been processed.
  * Result code 52005 may also be returned when the client is not receiving a JSS-related benefit,
    the benefit is not in an eligible status, or the processing date is outside the reapplication period.


  @positive
  Scenario Outline: Compare SC531 successful JSS reapplication responses
    Given I create the api payload for <condition>
    And   I send establish entitlement request to IIB endpoint
    And   I send establish entitlement request to Azure endpoint
    Then  I can see the SC531 responses are identical

    Examples:
      | condition                |
      | successful_reapplication |
#      | successful_reapplication_suspended |


  @negative @transaction
  Scenario Outline: Compare SC531 unsuccessful JSS reapplication responses
    Given I create the api payload for <condition>
    And   I send establish entitlement request to IIB endpoint
    And   I send establish entitlement request to Azure endpoint
    Then  I can see the SC531 responses are identical

    Examples:
      | condition                  |
      | unsuccessful_reapplication |
#      | successful_reapplication_suspended |


  @negative @authentication
  Scenario: Compare SC531 response for an unrecognised user
    Given I create the api payload for user_not_recognised
    And   I send establish entitlement request to IIB endpoint
    And   I send establish entitlement request to Azure endpoint
    Then  I can see the SC531 responses are identical


  @negative @client-validation
  Scenario: Compare SC531 response for an unrecognised client
    Given I create the api payload for client_not_recognised
    And   I send establish entitlement request to IIB endpoint
    And   I send establish entitlement request to Azure endpoint
    Then  I can see the SC531 responses are identical


  @negative @reassessment-validation
  Scenario Outline: Compare SC531 response when the client is not eligible for reassessment
    Given I create the api payload for <condition>
    And   I send establish entitlement request to IIB endpoint
    And   I send establish entitlement request to Azure endpoint
    Then  I can see the SC531 responses are identical

    Examples:
      | condition                      |
      | non_jss_benefit                |
      | benefit_not_in_eligible_status |
      | outside_reapplication_period   |
      | reassessment_already_completed |
