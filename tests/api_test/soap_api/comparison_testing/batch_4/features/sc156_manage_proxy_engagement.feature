@AZURE-SOAP-API @SOAP-API @sc156-comparison @comparison
Feature: Comparison Testing - SC156 - Manage Proxy Engagement

  As a client
  I want to send SC156 manage proxy engagement requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * Successful proxy creation returns 15600 - Transaction Successful
    * Unsuccessful business validation scenarios return 15699
    * Invalid client number format returns an XML validation error
    * Multiple proxy records can be created for the same client in a single request


  @positive @sc156-positive
  Scenario Outline: Compare SC156 successful responses between IIB and Azure
    Given I create the SC156 api payload for <condition>
    When  I send SC156 request to IIB endpoint
    And   I send SC156 request to Azure endpoint
    Then  I can see all the responses are identical for SC156

    Examples:
      | condition                 |
      | all_proxy_records_created |


  @negative @sc156-negative
  Scenario Outline: Compare SC156 unsuccessful responses between IIB and Azure
    Given I create the SC156 api payload for <condition>
    When  I send SC156 request to IIB endpoint
    And   I send SC156 request to Azure endpoint
    Then  I can see all the responses are identical for SC156

    Examples:
      | condition                 |
      | invalid_client_number     |
      | invalid_request_parameter |
      | client_not_recognised     |
      | no_current_js             |
      | missing_source_system     |
      | user_not_recognised       |
      | proxy_creation_failure    |
