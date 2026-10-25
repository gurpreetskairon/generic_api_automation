@REST-API
Feature: Integration - Get Jobseeker profile

  As a client
  I want to want to test the API functionality for getting the jobseeker profile status
  So that I can see the responses from the server

  The user can get the following status:
  * 200 - Completed
  * 200 - Incomplete
  * 400 - Invalid
  * 500 - Internal Server Error

  Scenario Outline: Check the status of getting jobseeker profile
    Given I send a request with <status>
    Then  I can see status <codes> in the response and the response body should match the expected <expected_result>
    Examples:
      | status                | codes | expected_result       |
      | Completed             | 200   | completed_profile     |
      | Incomplete            | 200   | incomplete_profile    |
      | Invalid               | 400   | internal_server_error |
      | Internal Server Error | 500   | invalid_request       |
