@AZURE-SOAP-API @SOAP-API @sc587-comparison
Feature: Comparison Testing - SC587 - Inquire SWIFTT User

  As a client
  I want to send SC587 Inquire SWIFTT User requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 58700 - Transaction Successful
      * 58701 - No district code found for the requested user - not able to find suitable data
      * 58702 - No SWIFTT user found for the requested user id


  @positive @sc587-positive
  Scenario Outline: Compare SC587 successful responses between IIB and Azure
    Given I create the SC587 api payload for <condition>
    When  I send SC587 request to IIB endpoint
    And   I send SC587 request to Azure endpoint
    Then  I can see all the responses are identical for SC587

    Examples:
      | condition           |
      | successful_response |


  @negative @sc587-negative
  Scenario Outline: Compare SC587 unsuccessful responses between IIB and Azure
    Given I create the SC587 api payload for <condition>
    When  I send SC587 request to IIB endpoint
    And   I send SC587 request to Azure endpoint
    Then  I can see all the responses are identical for SC587

    Examples:
      | condition               |
#      | district_code_not_found |
      | swiftt_user_not_found   |
