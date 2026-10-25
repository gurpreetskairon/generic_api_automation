@AZURE-REST-API @REST-API @sc263-comparison
Feature: Comparison Testing - SC263 - Get Client Identity Token Registration

  As a client,
  I want to send SC263 get client identity token registration requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected HTTP/result codes are:
      * 200 / 26300 - Transaction successful
      * 400 / 26301 - Invalid Request
      * 401 - Unauthorised
      * 500 / 26302 - Unexpected error, with additional details if available
      * 500 - Internal Server Error

  @positive @sc263-positive
  Scenario Outline: Compare SC263 successful responses between IIB and Azure
    Given I create the SC263 api payload for <condition>
    When I send SC263 request to IIB endpoint
    And I send SC263 request to Azure endpoint
    Then I can see all the responses are identical for SC263

    Examples:
      | condition           |
      | successful_response |

  @negative @sc263-negative
  Scenario Outline: Compare SC263 unsuccessful responses between IIB and Azure
    Given I create the SC263 api payload for <condition>
    When I send SC263 request to IIB endpoint
    And I send SC263 request to Azure endpoint
    Then I can see all the responses are identical for SC263

    Examples:
      | condition                    |
      | invalid_token_type           |
      | invalid_client_number_format |
      | authentication_failed        |

  @exception @sc263-exception
  Scenario Outline: Compare SC263 exception responses between IIB and Azure
    Given I create the SC263 api payload for <condition>
    When I send SC263 request to IIB endpoint
    And I send SC263 request to Azure endpoint
    Then I can see all the responses are identical for SC263

    Examples:
      | condition            |
      | unexpected_exception |
