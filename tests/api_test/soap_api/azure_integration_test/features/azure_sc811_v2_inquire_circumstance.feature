@AZURE-SOAP-API @SOAP-API @sc811v2-integration
Feature: Azure Integration - SC811V2 - Inquire Circumstance

  As a client
  I want to send SOAP requests to the Azure SC811 endpoint
  So that I can validate the response returned for inquiring client circumstances.

  # SC811 returns current or historical client circumstance details including
  # income, overseas pensions, allowable costs, family circumstances and
  # health circumstances.

   #  SC811 Test Data Notes

    #- Success (81100): Valid client and valid SWIFTT user.
    #- No Matching Record (81103): Client does not exist.
    #- Invalid Request (81101): Triggered by an invalid request payload (no special test data required).
    #- Client Not Recognised (81102): Invalid client number.
    #- Client Lock Not Held (81105): Valid client with errorIfNotLocked=true.
    #- Invalid SWIFTT User Code (81106): User ID omitted from the request.
    #- SWIFTT User Code Not Found (81110): Valid CNP ID with no associated SWIFTT user code (retrieveSwifttUser=true).
    #- CNP ID Not Recognised (81109): Invalid CNP ID (retrieveSwifttUser=true).
    #- User Code Not Found (81111): Invalid SWIFTT user code (e.g. INVALIDUSER).
    #- Result Not Recognised (80099): Client where SWIFTT returns provider result 20027 ("Secured record, access denied").


  @positive
  Scenario Outline: Check SC811 successful transaction response
    Given I create the correct payload for SC811 with "<condition>"
    When  I send the SC811 request to the Azure endpoint
    Then  I can see the SC811 result code as "<result_code>"
    And   I can see the SC811 result message as "<result_message>"

    Examples:
      | condition          | result_code | result_message         |
      | success            | 81100       | Transaction Successful |
      | no_matching_record | 81103       | No matching record     |


  @negative
  Scenario Outline: Check SC811 unsuccessful transaction response
    Given I create the payload for SC811 with "<condition>"
    When  I send the SC811 request to the Azure endpoint
    Then  I can see the SC811 result code as "<result_code>"
    And   I can see the SC811 result message as "<result_message>"

    Examples:
      | condition                  | result_code | result_message                  |
      | invalid_request            | 81101       | Invalid Request                 |
      | client_not_recognised      | 81102       | Client not recognised           |
      | client_lock_not_held       | 81105       | Client lock not held            |
      | invalid_swiftt_user_code   | 81106       | Invalid SWIFTT User Code        |
      | result_not_recognised      | 80099       | Result Not Recognised           |
      | cnp_id_not_recognised      | 81109       | CNP ID not recognised           |
      | swiftt_user_code_not_found | 81110       | SWIFTT user code not found      |
      | user_code_not_found        | 81111       | User Code <user code> not found |
