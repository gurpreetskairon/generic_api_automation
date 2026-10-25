@AZURE-REST-API @REST-API @sc932-comparison
Feature: Comparison Testing - SC932 - Publish Outbound Call Request

  As a client,
  I want to send SC932 Publish Outbound Call Request requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 93200 - The update request was successful
      * 93240 - Invalid Request
    * The expected exception HTTP status codes may include:
      * 401 - Unauthorized
      * 500 - Internal Server Error
      * 504 - Gateway Timeout


  @positive
  @sc932-positive
  Scenario Outline: Compare SC932 successful responses between IIB and Azure
    Given I create the SC932 api payload for <condition>
    When  I send SC932 request to IIB endpoint
    And   I send SC932 request to Azure endpoint
    Then  I can see all the responses are identical for SC932

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc932-negative
  Scenario Outline: Compare SC932 unsuccessful responses between IIB and Azure
    Given I create the SC932 api payload for <condition>
    When  I send SC932 request to IIB endpoint
    And   I send SC932 request to Azure endpoint
    Then  I can see all the responses are identical for SC932

    Examples:
      | condition       |
      | invalid_request |


  @negative
  @sc932-exception
  Scenario: Compare SC932 authentication failure between IIB and Azure
    Given I create the SC932 api payload for authentication_failure
    When  I send SC932 authentication failure request to IIB endpoint
    And   I send SC932 authentication failure request to Azure endpoint
    Then  I can see SC932 authentication failure status is identical
