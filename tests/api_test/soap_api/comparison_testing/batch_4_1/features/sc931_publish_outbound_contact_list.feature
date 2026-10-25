@AZURE-REST-API @REST-API @SC931-comparison
Feature: Comparison Testing - SC931 - Publish Outbound Contact list

  As a client,
  I want to send SC931 Publish Outbound Contact list requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 93100 - The request was successful
      * 93140 - Invalid Request
    * The expected exception HTTP status codes may include:
      * 401 - Unauthorized
      * 500 - Internal Server Error
      * 504 - Gateway Timeout


  @positive
  Scenario Outline: Compare SC931 successful response for publishing a new request between IIB and Azure
    Given I create the SC931 api payload for <condition>
    When  I send SC931 request to IIB endpoint
    And   I send SC931 request to Azure endpoint
    Then  I can see all the responses are identical for SC931

    Examples:
      | condition              |
      | transaction_successful |


  @positive
  Scenario Outline: Compare SC931 successful responses for altering a existing Contact list between IIB and Azure
    Given I create the SC931 api payload for <condition>
    When  I send SC931 request to IIB endpoint
    And   I send SC931 request to Azure endpoint
    Then  I can see all the responses are identical for SC931

    Examples:
      | condition |
      | update    |
      | cancel    |


  @negative
  Scenario Outline: Compare SC931 unsuccessful responses between IIB and Azure
    Given I create the SC931 api payload for <condition>
    When  I send SC931 request to IIB endpoint
    And   I send SC931 request to Azure endpoint
    Then  I can see all the responses are identical for SC931

    Examples:
      | condition       |
      | invalid_request |


  @negative
  Scenario Outline: Compare SC931 exception responses between IIB and Azure
    Given I create the SC931 api payload for <condition>
    When  I send SC931 request to IIB endpoint
    And   I send SC931 request to Azure endpoint
    Then  I can see all the responses are identical for SC931

    Examples:
      | condition              |
      | authentication_failure |
#      | internal_server_error  |
#      | gateway_timeout        |
