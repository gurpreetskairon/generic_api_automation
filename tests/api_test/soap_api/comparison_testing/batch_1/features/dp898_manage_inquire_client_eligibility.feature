@AZURE-REST-API
@REST-API
@dp898-comparison
@inquireclienteligibility
Feature: Comparison Testing - DP898 - Inquire Client Eligibility

  As a MyMSD consumer,
  I want to send the same DP898 Inquire Client Eligibility request to DataPower and Azure
  So that I can confirm both endpoints return identical responses

  Acceptance:
  * Send the same DP898 request to the DataPower and Azure endpoints
  * Confirm that the DataPower and Azure responses are identical
  * Cover successful and unsuccessful request conditions


  @positive
  Scenario: Check whether the DP898 responses are the same across different endpoints
    Given I create the correct DP898 api payload
    When  I send the DP898 request to the DataPower endpoint
    And   I send the same DP898 request to the Azure endpoint
    Then  I can see the DP898 responses are identical


  @negative
  Scenario Outline: Check DP898 responses are the same across different endpoints with different conditions
    Given I create the DP898 api payload with different "<condition>"
    When  I send the DP898 request to the DataPower endpoint
    And   I send the same DP898 request to the Azure endpoint
    Then  I can see the DP898 responses are identical

    Examples:
      | condition             |
      | no_matching_client    |
      | invalid_client_number |
      | missing_client_number |
      | user_not_recognised   |
