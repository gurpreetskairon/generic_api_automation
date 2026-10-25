@AZURE-SOAP-API @SOAP-API @sc843-comparison
Feature: Comparison Testing - SC843 - Get Associated Postcodes

  As a client,
  I want to send SC843 requests to IIB and Azure
  So that I can verify both SOAP responses are identical

  @positive
  Scenario Outline: Compare SC843 successful transaction response
    Given I create the SC843 api payload for <condition>
    When I send SC843 request to IIB endpoint
    And I send SC843 request to Azure endpoint
    Then I can see all the responses are identical for SC843

    Examples:
      | condition              |
      | successful_transaction |
      | no_matching_record |

  
  @negative
  Scenario Outline: Compare SC843 invalid search criteria response
    Given I create the SC843 api payload for <condition>
    When I send SC843 request to IIB endpoint
    And I send SC843 request to Azure endpoint
    Then I can see all the responses are identical for SC843

    Examples:
      | condition               |
      | invalid_search_criteria |
