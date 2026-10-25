@SOAP-API
Feature: Comparison Testing - SC550 - Inquire participant

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  Acceptance:
  (1) The responses from the IIB and Azure endpoints are identical
  (2) 202 - Accepted


  @positive
  Scenario: Compare SC550 successful response
    Given I create the correct api payload
    And   I send the child support request to IIB endpoint
    And   I send the child support request to Azure endpoint
    Then  I can see the responses are identical


  @negative
  Scenario Outline: Compare SC550 responses when the request details contain missing values
    Given I create the api payload with different <conditions>
    And   I send the child support request to IIB endpoint
    And   I send the child support request to Azure endpoint
    Then  I can see the error responses are identical

    Examples:
      | conditions              |
      | missing applicant ird   |
      | missing applicant dob   |
      | missing other carer ref |


  @negative
  Scenario Outline: Compare SC550 responses when the request details contain invalid ird values
    Given I create the api payload with different <conditions>
    And   I send the child support request to IIB endpoint
    And   I send the child support request to Azure endpoint
    Then  I can see the error responses are identical

    Examples:
      | conditions              |
      | invalid applicant ird   |
      | invalid child ird       |
      | invalid other carer ird |
      | invalid applicant ird   |
      | invalid child ird       |
      | invalid other carer ird |


  @negative
  Scenario Outline: Compare SC550 responses when the request details contain invalid values
    Given I create the api payload with different <conditions>
    And   I send the child support request to IIB endpoint
    And   I send the child support request to Azure endpoint
    Then  I can see the error responses are identical

    Examples:
      | conditions           |
      | invalid dob          |
      | invalid trans id     |
      | invalid bank account |
      | invalid given name   |
