@REST-API
Feature: Integration - Check employer profile

  As a client
  I want to want to test the API functionality for employer profile
  So that I can see see the responses from the server

  The user can get the following status:
  * 202 - Accepted
  * 400 - Source header
  * 400 - Bad Request
  * 401 - Unauthorized
  * 400 - Empty payload
  * 404 - Method Not Allowed
  * 404 - Resource Not Found

  Scenario Outline: Check the status of employer profile
    Given I send a request with <status>
    Then  I can see status <codes> in the response and the response body should match the expected <expected_result>

    Examples:
      | status             | codes | expected_result    |
      | Accepted           | 202   | none               |
      | Source header      | 400   | Source_headers     |
      | Bad Request        | 400   | none               |
      | Unauthorized       | 401   | Unauthorized       |
      | Empty payload      | 400   | empty_payload      |
      | Method Not Allowed | 404   | method_not_allowed |
      | Resource Not Found | 404   | resource_not_found |
