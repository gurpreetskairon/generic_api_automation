@SOAP-API
Feature: Comparison Testing - SC551 - inquire child support service

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario: Compare SC551 successful response
    Given I create the correct api payload
    And   I send the child support request to IIB endpoint
    And   I send the child support request to Azure endpoint
    Then  I can see the responses are identical


  @negative
  Scenario Outline: Compare SC551 responses when the request details contain invalid values
    Given I create the api payload with different <conditions>
    And   I send the child support request to IIB endpoint
    And   I send the child support request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions                     |
      | invalid start month            |
      | invalid ird number             |
      | missing ird number             |
      | inactive liable parent account |
      | invalid date range             |
      | invalid start date             |
