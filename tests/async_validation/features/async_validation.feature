@async

Feature: Async API response validation
  As a tester, I want to validate the asynchronous responses of service
  contracts from the callback files, so that every callback file is
  executed and reported as its own scenario.

  Scenario: Validate an async response against expected data
    Given the callback file is loaded
    When I retrieve the async responses
    Then I should receive the expected response code
    And I validate the async response data
    And the callback file is cleaned up
