@AZURE-SOAP-API @SOAP-API @sc897-comparison

Feature: Comparison Testing - SC897 - Inquire User Activity

  As a client,
  I want to send SC897 Inquire User Activity requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 89700 - Transaction Successful
      * 89701 - No Matching Record
      * 89710 - Invalid Request


  @positive
  @sc897-positive
  Scenario Outline: Compare SC897 successful responses between IIB and Azure
    Given I create the SC897 api payload for <condition>
    When I send SC897 request to IIB endpoint
    And I send SC897 request to Azure endpoint
    Then I can see all the responses are identical for SC897

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc897-negative
  Scenario Outline: Compare SC897 unsuccessful responses between IIB and Azure
    Given I create the SC897 api payload for <condition>
    When I send SC897 request to IIB endpoint
    And I send SC897 request to Azure endpoint
    Then I can see all the responses are identical for SC897

    Examples:
      | condition          |
      | no_matching_record |
      | invalid_request    |
