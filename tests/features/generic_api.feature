Feature: Generic API request validation
  As a tester, I want to drive API tests from a CSV file so that every
  row is executed and reported as its own scenario, without writing a
  new feature/step for every endpoint.

  Scenario: Validate an API response against expected data
    Given I fetch the endpoint
    And the request information
    When I send the request
    Then I should receive the expected status code
    And I validate the response data
