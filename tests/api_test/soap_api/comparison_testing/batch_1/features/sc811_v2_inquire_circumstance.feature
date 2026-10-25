@IIB-AZURE-COMPARISON @SOAP-API @sc811v2-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC811V2 - Inquire Circumstance

  # SC811 V2 Test Data Notes
  #
  # - Success (81100): Valid client and valid SWIFTT user.
  # - No Matching Record (81103): Client does not exist.
  # - Invalid Request (81101): Triggered by an invalid request payload (no special test data required).
  # - Client Not Recognised (81102): Invalid client number.
  # - Client Lock Not Held (81105): Valid client with errorIfNotLocked=true.
  # - Invalid SWIFTT User Code (81106): User ID omitted from the request.
  # - SWIFTT User Code Not Found (81110): Valid CNP ID with no associated SWIFTT user code (retrieveSwifttUser=true).
  # - CNP ID Not Recognised (81109): Invalid CNP ID (retrieveSwifttUser=true).
  # - User Code Not Found (81111): Invalid SWIFTT user code (e.g. INVALIDUSER).
  # - Result Not Recognised (80099): Client where SWIFTT returns provider result 20027 ("Secured record, access denied").


  @positive
  Scenario Outline: Compare SC811V2 successful transaction response
    Given I create the correct payload for SC811V2 with "<condition>"
    And   I send the SC811V2 request to IIB endpoint
    And   I send the SC811V2 request to Azure endpoint
    Then  I can see all the responses are identical for SC811V2

    Examples:
      | condition          |
      | success            |
      | no_matching_record |


  @negative
  Scenario Outline: Compare SC811V2 unsuccessful transaction response
    Given I create the payload for SC811V2 with "<condition>"
    And   I send the SC811V2 request to IIB endpoint
    And   I send the SC811V2 request to Azure endpoint
    Then  I can see all the responses are identical for SC811V2

    Examples:
      | condition                  |
      | invalid_request            |
      | client_not_recognised      |
      | client_lock_not_held       |
      | invalid_swiftt_user_code   |
      | cnp_id_not_recognised      |
      | swiftt_user_code_not_found |
      | user_code_not_found        |
      | result_not_recognised      |
