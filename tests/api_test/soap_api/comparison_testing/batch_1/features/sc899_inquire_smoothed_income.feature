@AZURE-SOAP-API @SOAP-API @sc899-comparison
@INQUIRESMOOTHEDINCOME
Feature: Comparison Testing - SC899 - Inquire Eligibility

As a consumer of the SC899 SOAP service
I want to compare the SC899 response between Azure and IIB
So that I can confirm Azure behaves like-for-like with IIB for the agreed scenarios

The user can get the following status:

* 89900 - Transaction Successful
* 899003 - No matching record
* 89909 - User not recognised
* 89999 - Result Not Recognised

Notes:
* uses a CSPO client, automation sanity script "test_sanity_cspo_via_cms" can be used to create the client data


  @positive
  Scenario: Compare SC899 successful responses between Azure and IIB
    Given I created the correct SC899 api payload
    And   I send the request to the IIB endpoint
    And   I send the request to the Azure endpoint
    Then  I can see the responses are identical


  @positive
  Scenario Outline: Compare SC899 successful responses between Azure and IIB with conditions
    Given I create the correct SC899 api payload with <conditions>
    And   I send the request to the IIB endpoint
    And   I send the request to the Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions          |
      | no_matching_record  |
      | user_not_recognised |
