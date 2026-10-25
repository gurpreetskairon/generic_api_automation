@AZURE-SOAP-API @SOAP-API @DP840-comparison
Feature: Comparison Testing - DP840 - Find Address
  As a client,
  I want to send DP840 Find Address requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical



  @positive @DP840-positive
  Scenario Outline: Compare DP840 successful responses between IIB and Azure
    Given I create the DP840 api payload for <condition>
    When I send DP840 request to IIB endpoint
    And I send DP840 request to Azure endpoint
    Then I can see all the responses are identical for DP840

    Examples:
      | condition                        |
      | transaction_successful           |
      | no_matching_record               |

#  @negative @DP840-negative
#  Scenario Outline: Compare DP840 invalid search responses between IIB and Azure
#    Given I create the DP840 api payload for <condition>
#    When I send DP840 request to IIB endpoint
#    And I send DP840 request to Azure endpoint
#    Then I can see all the responses are identical for DP840
#
#    Examples:
#      | condition             |
#      | invalid_search        |
