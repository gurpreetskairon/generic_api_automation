@AZURE-REST-API @REST-API @dp605-integration @notify_special_caution
@manageclientnotification
Feature: Azure Integration - DP605 - Notify Special Caution

As a consumer of the DP605 REST service
I want to validate successful and unsuccessful notify special caution responses
So that the Azure integration behaves according to the service specification and acceptance criteria

AC coverage:
* Positive scenario validates that a valid client number returns result code 82900 and message Transaction Successful
* Negative scenario validates that an invalid numeric non-existing client number returns result code 82902 and message Client not recognised

The user can get the following status:

* 82900 - Transaction Successful
* 82902 - Client not recognised

This service allows STAR to notify CMS of a special caution for a client.

DP605 supports STAR special caution types such as:

* LWAR - Warning letter issued
* TREP - Trespass order


  @positive @result_code_82900 @successful_response
  Scenario Outline: Check DP605 successful notify special caution response
    Given I created the correct DP605 notify special caution payload for STAR with category "<category_code>" and type "<type_code>"
    And   I used a valid client number as the DP605 path parameter
    When  I send the DP605 notify special caution request to the Azure endpoint
    Then  I can see the "Transaction Successful" response returned
    And   I can see HTTP status code <http_status_code> returned
    And   I can see result code <result_code> returned in the JSON response
    And   I can see result message "<result_message>" returned in the JSON response

    Examples:
      | category_code      | type_code | result_code | http_status_code | result_message         |
      | STAFFSECURITYALERT | LWAR      | 82900       | 201              | Transaction Successful |
      | STAFFSECURITYALERT | TREP      | 82900       | 201              | Transaction Successful |


  @negative @invalid_client_number @client_not_recognised
  Scenario Outline: Check DP605 unsuccessful response for invalid client number
    Given I created the correct DP605 notify special caution payload for STAR with category "<category_code>" and type "<type_code>"
    And   I used an invalid client number as the DP605 path parameter
    When  I send the DP605 notify special caution request to the Azure endpoint
    Then  I can see HTTP status code <http_status_code> returned
    And   I can see result code <result_code> returned in the JSON response
    And   I can see result message "<result_message>" returned in the JSON response

    Examples:
      | category_code      | type_code | result_code | http_status_code | result_message        |
      | STAFFSECURITYALERT | LWAR      | 82902       | 470              | Client not recognised |
      | STAFFSECURITYALERT | TREP      | 82902       | 470              | Client not recognised |
