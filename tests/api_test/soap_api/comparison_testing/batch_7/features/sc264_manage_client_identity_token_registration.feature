@AZURE-REST-API @REST-API @sc264-comparison
Feature: Comparison Testing - SC264 - Manage Client Identity Token Registration

  As a client,
  I want to send SC264 manage client identity token registration requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected HTTP/result codes are:
      * 200 / 26400 - Transaction successful
      * 400 / 26401 - Invalid Request
      * 401 - Unauthorised
      * 500 / 26402 - Unexpected error, with additional details if available

  @positive @sc264-positive
  Scenario Outline: Compare SC264 successful responses between IIB and Azure
    Given I create the SC264 api payload for <condition>
    When I send SC264 request to IIB endpoint
    And I send SC264 request to Azure endpoint
    Then I can see all the responses are identical for SC264

    Examples:
      | condition           |
      | successful_response |

  @negative @sc264-negative
  Scenario Outline: Compare SC264 unsuccessful responses between IIB and Azure
    Given I create the SC264 api payload for <condition>
    When I send SC264 request to IIB endpoint
    And I send SC264 request to Azure endpoint
    Then I can see all the responses are identical for SC264

    Examples:
      | condition                    |
      | invalid_token_type           |
      | invalid_client_number_format |
      | authentication_failed        |

  @exception @sc264-exception
  Scenario Outline: Compare SC264 exception responses between IIB and Azure
    Given I create the SC264 api payload for <condition>
    When I send SC264 request to IIB endpoint
    And I send SC264 request to Azure endpoint
    Then I can see all the responses are identical for SC264

    Examples:
      | condition            |
      | unexpected_exception |

  # Execution Note:
  # Service unavailable / HTTP 500 Internal Server Error is excluded from automation
  # because this condition cannot be reliably reproduced.
