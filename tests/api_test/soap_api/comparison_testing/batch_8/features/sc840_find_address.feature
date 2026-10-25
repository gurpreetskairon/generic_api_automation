@AZURE-SOAP-API @SOAP-API @sc840-comparison
Feature: Comparison Testing - SC840 - Find Address
  As a client,
  I want to send SC840 Find Address requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical



  @positive @SC840-positive
  Scenario Outline: Compare SC840 successful responses between IIB and Azure
    Given I create the SC840 api payload for <condition>
    When I send SC840 request to IIB endpoint
    And I send SC840 request to Azure endpoint
    Then I can see all the responses are identical for SC840

    Examples:
      | condition                        |
      | transaction_successful           |
      | no_matching_record               |

  @negative @SC840-negative
  Scenario Outline: Compare SC840 invalid search responses between IIB and Azure
    Given I create the SC840 api payload for <condition>
    When I send SC840 request to IIB endpoint
    And I send SC840 request to Azure endpoint
    Then I can see all the responses are identical for SC840

    Examples:
      | condition             |
      | invalid_search        |
