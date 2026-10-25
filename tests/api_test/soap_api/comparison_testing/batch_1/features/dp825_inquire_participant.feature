@REST-API
@DATAPOWER-API
@DP825
@DP825-COMPARISON
Feature: Comparison Testing - DP825 - Inquire Client

  As a MyMSD consumer,
  I want to compare the responses from IIB and Azure
  So that I can confirm the responses are identical

  Acceptance:
  * Send the same DP825 request to the IIB and Azure endpoints
  * Confirm that the IIB and Azure responses are identical
  * Cover successful and no-matching-client conditions


  @positive
  Scenario: Check whether the DP825 responses are the same across different endpoints
    Given I create the DP825 request for "valid_client"
    When  I send the DP825 request to the IIB endpoint
    And   I send the same DP825 request to the Azure endpoint
    Then  I can see the DP825 responses are identical


  @negative
  Scenario Outline: Check DP825 responses are the same across different endpoints with different conditions
    Given I create the DP825 request for "<condition>"
    When  I send the DP825 request to the IIB endpoint
    And   I send the same DP825 request to the Azure endpoint
    Then  I can see the DP825 responses are identical

    Examples:
      | condition          |
      | no_matching_client |
