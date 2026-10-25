@AZURE-REST-API @REST-API @sc933-comparison
Feature: Comparison Testing - SC933 - Publish Outbound Campaign Control

  As a client,
  I want to send SC933 Publish Outbound Campaign Control requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 93300 - Campaign control action was successful
      * 93340 - Invalid Request
      * 93341 - Returned for 4xx HTTP responses
      * 93350 - Returned for 5xx HTTP responses
    * The expected exception HTTP status codes may include:
      * 401 - Unauthorized
      * 500 - Internal Server Error
      * 504 - Gateway Timeout

  Execution Note:
    * Exception scenarios will be automated once reliable conditions to reproduce the 401, 500 and 504 responses are confirmed.


  @positive
  @sc933-positive
  Scenario Outline: Compare SC933 successful start and stop responses between IIB and Azure
    Given I create the SC933 api payload for <condition>
    And   I ensure SC933 campaign is stopped before comparison
    When  I send SC933 request with start operation to IIB endpoint
    And   I send SC933 request with stop operation to IIB endpoint
    And   I send SC933 request with start operation to Azure endpoint
    And   I send SC933 request with stop operation to Azure endpoint
    Then  I can see SC933 start and stop responses are identical between IIB and Azure

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc933-negative
  Scenario Outline: Compare SC933 unsuccessful responses between IIB and Azure
    Given I create the SC933 api payload for <condition>
    When  I send SC933 request to IIB endpoint
    And   I send SC933 request to Azure endpoint
    Then  I can see all the responses are identical for SC933

    Examples:
      | condition                |
      | invalid_request          |
      | campaign_already_stopped |


  @negative
  @sc933-authentication
  Scenario: Compare SC933 authentication failure between IIB and Azure
    Given I create the SC933 api payload for authentication_failure
    When  I send SC933 authentication failure request to IIB endpoint
    And   I send SC933 authentication failure request to Azure endpoint
    Then  I can see SC933 authentication failure status is identical
