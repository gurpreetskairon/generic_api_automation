@REST-API
Feature: Integration - Update Obman or Salesforce from SWIFTT

  As a user
  I want to publish and sync obligations in obman/salesforce
  So that I can see the responses from the server

  The user can get the following status:
  * 200 - published
  * 200 - syncd

  Scenario Outline: AIS publish obligation
    Given I send an api request with <body> body to publish a clients obligations
    Then  I can see status <codes> in the response and the response body should match the expected <expected_result>
    Examples:
      | body        | codes | expected_result        |
      | default     | 200   | ais_publish_obligation |
      | null_values | 200   | ais_publish_obligation |


  Scenario Outline: AIS sync obligation
    Given I send an api request with <body> body to sync a clients obligations
    Then  I can see status <codes> in the response and the response body should match the expected <expected_result>
    Examples:
      | body        | codes | expected_result                |
      | default     | 200   | Payload processed successfully |
      | null_values | 200   | Payload processed successfully |


  Scenario Outline: Obman sync direct
    Given I send an api request to obman
    Then  I can see status <codes> in the response and the response body should match the expected <expected_result>
    Examples:
      | codes | expected_result                |
      | 200   | Payload processed successfully |
