@AZURE-SOAP-API @SOAP-API @sc808-comparison
@findclientforuniqueidentifier
Feature: Comparison Testing - SC808 - Find client for unique identifier

  As a consumer of the SC808 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC808 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC808 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * A matching bank account or Community Services Card search returns result code 80800 and message Transaction Successful.
  * A request where no matching client exists returns result code 80801 and message No matching record.
  * A request containing a building society bank account returns result code 80802 and message Bank account sent belongs to a building society.

  Execution notes:
  * The same payload is sent to both IIB and Azure for each comparison scenario.
  * Only one search criterion is populated in each request: bank account number or Community Services Card number.
  * A bank account search may return more than one matching client.
  * A Community Services Card search returns only one matching client.
  * No validation is performed by the service on the bank account or Community Services Card number.


  @positive
  Scenario Outline: Compare SC808 successful responses
    Given I create the SC808 api payload for <condition>
    When  I send SC808 find client request to IIB endpoint
    And   I send SC808 find client request to Azure endpoint
    Then  I can see all the responses are identical for SC808

    Examples:
      | condition                                |
      | successful_bank_account_search           |
      | successful_community_service_card_search |


  @negative
  Scenario Outline: Compare SC808 unsuccessful search responses
    Given I create the SC808 api payload for <condition>
    When  I send SC808 find client request to IIB endpoint
    And   I send SC808 find client request to Azure endpoint
    Then  I can see all the responses are identical for SC808

    Examples:
      | condition                |
      | no_matching_record       |
      | building_society_account |
