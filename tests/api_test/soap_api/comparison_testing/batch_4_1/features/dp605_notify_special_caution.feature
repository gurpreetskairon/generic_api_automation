@AZURE-REST-API @REST-API @dp605-comparison @notify_special_caution
@manageclientnotification
Feature: Comparison Testing - DP605 - Notify Special Caution

  As a consumer of the DP605 REST service
  I want to compare Azure and IIB responses for notify special caution
  So that the Azure implementation behaves consistently with existing IIB behaviour

  Acceptance:
  * Azure and IIB responses should be identical for the covered DP605 comparison scenarios.
  * DP605 is a REST service and returns JSON responses.
  * Detailed field-level validation of result code and result message is covered under Azure integration testing.
  * Comparison testing validates that Azure and IIB return the same HTTP status code and JSON response body for the same DP605 request condition.

  Notes:
  * This service allows STAR to notify CMS of a special caution for a client.
  * DP605 supports STAR special caution types such as LWAR and TREP.
  * LWAR - Warning letter issued.
  * TREP - Trespass order.


  @positive @result_code_82900 @successful_response @azure_iib_comparison
  Scenario Outline: Compare DP605 successful notify special caution response between Azure and IIB
    Given I created the correct DP605 notify special caution payload for STAR with category "<category_code>" and type "<type_code>"
    And   I used a valid client number as the DP605 path parameter
    When  I send the DP605 notify special caution request to the Azure endpoint
    And   I send the DP605 notify special caution request to the IIB endpoint
    Then  I can see all the responses are identical for DP605

    Examples:
      | category_code      | type_code |
      | STAFFSECURITYALERT | LWAR      |
      | STAFFSECURITYALERT | TREP      |


  @negative @invalid_client_number @client_not_recognised @azure_iib_comparison
  Scenario Outline: Compare DP605 invalid client number response between Azure and IIB
    Given I created the correct DP605 notify special caution payload for STAR with category "<category_code>" and type "<type_code>"
    And   I used an invalid client number as the DP605 path parameter
    When  I send the DP605 notify special caution request to the Azure endpoint
    And   I send the DP605 notify special caution request to the IIB endpoint
    Then  I can see all the responses are identical for DP605

    Examples:
      | category_code      | type_code |
      | STAFFSECURITYALERT | LWAR      |
      | STAFFSECURITYALERT | TREP      |
