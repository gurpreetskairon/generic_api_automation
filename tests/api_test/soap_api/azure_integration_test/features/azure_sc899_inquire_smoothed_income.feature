@AZURE-SOAP-API @SOAP-API @sc899-comparison
@INQUIRESMOOTHEDINCOME
Feature: Azure Integration - SC899 - Inquire Eligibility

As a consumer of the SC899 SOAP service
I want to verify the SC899 azure response
So that I can confirm the Azure responses matches whats expected

The user can get the following status:

* 89900 - Transaction Successful
* 899003 - No matching record
* 89909 - User not recognised
* 89999 - Result Not Recognised

Notes:
* uses a CSPO client, automation sanity script "test_sanity_cspo_via_cms" can be used to create the client data


  @positive
  Scenario Outline: Verify SC899 successful responses between Azure and IIB
    Given I created the correct SC899 api payload
    And   I send the request to the Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | result_code | result_message         |
      | 89900       | Transaction Successful |


  @positive
  Scenario Outline: Verify SC899 successful responses between Azure and IIB with conditions
    Given I create the correct SC899 api payload with <conditions>
    And   I send the request to the Azure endpoint
    Then  I can see result code <result_code> is the same in both responses
    And   I can see result message <result_message> is the same in both responses

    Examples:
      | result_code | result_message      | conditions          |
      | 899003      | No matching record  | no_matching_record  |
      | 89909       | User not recognised | user_not_recognised |
#      | 89999       | Result Not Recognised  | result_not_recognised   |
