@SOAP-API
Feature: Comparison Testing - SC346 - Advise Application Shortlist

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC346 responses are identical


  @skip @positive
  Scenario Outline: Compare SC346 successful transaction response
    Given I create the correct SC346 api payload with different <conditions>
    When  I send the SC346 request to IIB endpoint
    And   I send the SC346 request to Azure endpoint
    Then  I can see all the responses are identical for SC346

    Examples:
      | conditions             |
      | successful_transaction |
