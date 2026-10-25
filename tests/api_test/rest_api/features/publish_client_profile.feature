@REST-API
Feature: Integration - Publish client profile

  As a client
  I want to test the API functionality for publishing client profiles
  So that I can see see the responses from the server

  (1) The user can get the following status:

  * 202 - Accepted
  * 401 - Key missing
  * 400 - Header missing
  * 400 - Body missing

  (2) The user can publish the client profile successfully

  Scenario Outline: Check the status of publishing client profile
    Given I send a request with <status>
    Then  I can see status <codes> in the response and the response body should match the expected <expected_result>
    Examples:
      | status         | codes | expected_result          |
      | Accepted       | 202   | none                     |
      | Key missing    | 401   | SubscriptionKey_NotFound |
      | Header missing | 400   | Missing_headers          |
      | Body missing   | 400   | empty_payload            |
