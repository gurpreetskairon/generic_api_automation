@SOAP-API @DP823
Feature: Comparison Testing - DP823 - Create unstructured note

As a client
I want to compare the responses from the IIB and Azure
So that I can see whether the responses are identical

Acceptance:
  * The responses from the IIB and Azure endpoints are identical
  * The expected result codes are:
    * 82300 - Transaction Successful
    * 90004 - Invalid credential
    * 90003 - Invalid request content

Execution Note:
  * The unsuccessful transaction scenario is not covered in automation as there are
    no available logs or test conditions to reproduce the scenario.
  * This scenario will be covered through manual or functional testing.


  @positive
  Scenario: Compare DP823 successful transaction response
    Given I create the api payload for successful_response
    And   I send create unstructured note request to IIB endpoint
    And   I send create unstructured note request to Azure endpoint
    Then  I can see the DP823 responses are identical


  @negative @authentication
  Scenario: Compare DP823 response for invalid user credentials
    Given I create the api payload for user_not_recognised
    And   I send create unstructured note request to IIB endpoint
    And   I send create unstructured note request to Azure endpoint
    Then  I can see the DP823 responses are identical


  @negative @client-validation
  Scenario: Compare DP823 response for an invalid client number
    Given I create the api payload for client_not_recognised
    And   I send create unstructured note request to IIB endpoint
    And   I send create unstructured note request to Azure endpoint
    Then  I can see the DP823 responses are identical


  @negative @invalid-request
  Scenario Outline: Compare DP823 invalid request responses
    Given I create the api payload for <condition>
    And   I send create unstructured note request to IIB endpoint
    And   I send create unstructured note request to Azure endpoint
    Then  I can see the DP823 responses are identical

    Examples:
      | condition                                 |
      | note_text_over_4000_characters            |
      | note_text_with_special_characters         |
      | short_description_over_100_characters     |
      | short_description_with_special_characters |
