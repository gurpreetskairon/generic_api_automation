@REST-API
Feature: Integration - Check event notifications

  As a client
  I want to want to test the API functionality for event notifications
  So that I can see the responses from the server

  (1) The user can get the following status:

  * 200 - success
  * 400 - Incomplete
  * 500 - Internal Server Error

  (2) The user can send options method
  (3) The user can validate handshake

  Scenario Outline: Check the status of event notifications
    Given I send a request with <status>
    Then  I can see the <status> and <codes> in the response and the response body should match the expected <expected_result>
    Examples:
      | status                | codes | expected_result      |
      | success               | 200   | success              |
      | bad request           | 400   | none                 |
      | Internal Server Error | 500   | none                 |
      | validate handshake    | 200   | handshake_validation |
      | options               | 200   | none                 |
