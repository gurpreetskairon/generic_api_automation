@AZURE-REST-API @REST-API @sc154-comparison
Feature: Comparison Testing - SC154 - Manage Non-Financial Sanctions Upskilling

  As a client,
  I want to send SC154 Manage Non-Financial Sanctions Upskilling requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected HTTP result codes and messages are:
      * 200 - The get request was successful
      * 400 - The data request is invalid. Check the error message for further information and resend the request with the corrected data
      * 404 - The requested resource was not found


  @positive @sc154-positive
  Scenario Outline: Compare SC154 successful responses between IIB and Azure
    Given I create the SC154 api payload for <condition>
    When I send SC154 request to IIB endpoint
    And I send SC154 request to Azure endpoint
    Then I can see all the responses are identical for SC154

    Examples:
      | condition           |
      | successful_response |


  @negative @sc154-negative
  Scenario Outline: Compare SC154 unsuccessful responses between IIB and Azure
    Given I create the SC154 api payload for <condition>
    When I send SC154 request to IIB endpoint
    And I send SC154 request to Azure endpoint
    Then I can see all the responses are identical for SC154

    Examples:
      | condition                     |
      | resource_not_found            |
      | missing_client_number         |
      | missing_upskilling_id         |

