@SOAP-API @childsupport
Feature: Azure Integration - SC550 - Inquire participant

  As a client
  I want to verify the responses from the Azure
  So that I can see whether the responses are what we expected

  Acceptance:
  (1) The responses from the Azure endpoints are what we expected
  (2) The user can get the following status:
      * 202 - Accepted


  @positive
  Scenario Outline: Verify azure SC550 successful response
    Given I create the correct api payload
    And   I send the child support request to Azure endpoint
    Then  I see the response status code matches the expected code <status_code>

    Examples:
      | status_code |
      | 202         |


  @negative
  Scenario Outline: Verify azure SC550 responses when the request details contain missing values
    Given I create the api payload with different <conditions>
    And   I send the child support request to Azure endpoint
    Then  I see the response status code matches the expected code <status_code>
    And   I see the response body matches the expected response body

    Examples:
      | conditions              | status_code |
      | missing applicant ird   | 400         |
      | missing applicant dob   | 400         |
      | missing other carer ref | 400         |
      | missing trans id        | 400         |


  @negative
  Scenario Outline: Verify azure SC550 responses when the request details contain invalid ird values
    Given I create the api payload with different <conditions>
    And   I send the child support request to Azure endpoint
    Then  I see the response status code matches the expected code <status_code>
    And   I see the response body matches the expected response body

    Examples:
      | conditions              | status_code |
      | invalid applicant ird   | 400         |
      | invalid child ird       | 400         |
      | invalid other carer ird | 400         |
      | invalid applicant ird   | 400         |
      | invalid child ird       | 400         |
      | invalid other carer ird | 400         |


  @negative
  Scenario Outline: Verify azure SC550 responses when the request details contain invalid values
    Given I create the api payload with different <conditions>
    And   I send the child support request to Azure endpoint
    Then  I see the response status code matches the expected code <status_code>
    And   I see the response body matches the expected response body

    Examples:
      | conditions           | status_code |
      | invalid dob          | 400         |
      | invalid trans id     | 400         |
      | invalid bank account | 400         |
      | invalid given name   | 400         |
