Feature: Comparison Testing - SC152 Manage Job Search Activity

  As a client
  I want to send SC152 requests to the IIB and Azure endpoints
  So that I can verify the responses are identical


  Scenario Outline: Compare SC152 successful transaction response
    Given I create the correct SC152 api request with different <conditions>
    And I send the SC152 request to IIB endpoint
    And I send the SC152 request to Azure endpoint
    Then I can see all the responses are identical for SC152

    Examples:
      | conditions             |
      | successful_transaction |


  Scenario Outline: Compare SC152 invalid request response
    Given I create the correct SC152 api request with different <conditions>
    And I send the SC152 request to IIB endpoint
    And I send the SC152 request to Azure endpoint
    Then I can see all the responses are identical for SC152

    Examples:
      | conditions      |
      | invalid_request |


  Scenario Outline: Compare SC152 successful update response
    Given I create the correct SC152 update api request with different <conditions>
    And I send the SC152 update request to IIB endpoint
    And I send the SC152 update request to Azure endpoint
    Then I can see all the SC152 update responses are identical

    Examples:
      | conditions        |
      | successful_update |


  Scenario Outline: Compare SC152 invalid update response
    Given I create the correct SC152 update api request with different <conditions>
    And I send the SC152 update request to IIB endpoint
    And I send the SC152 update request to Azure endpoint
    Then I can see all the SC152 update responses are identical

    Examples:
      | conditions     |
      | invalid_update |
