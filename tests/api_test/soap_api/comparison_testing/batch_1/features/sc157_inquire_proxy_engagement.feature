@SOAP-API
Feature: Comparison Testing - SC157 - Inquire proxy engagement

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario: Compare SC157 successful response
    Given I create the correct api payload
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical


  @negative
  Scenario Outline: Compare SC157 responses with invalid data
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions            |
#      |client_not_recognised  |  https://msd-jira-cloud.atlassian.net/browse/API-3450
      |no_js_service          |
      |no_source_system       |
      |invalid_user_code      |
      |alpha_numeric_client_number |
