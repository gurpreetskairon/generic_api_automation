@comparison
Feature: Comparison Testing - SC881 - Manage Application

  As a client
  I want to send SC881 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC881 successful responses between IIB and Azure
    Given I create the SC881 api payload for <condition>
    When  I send SC881 request to IIB endpoint
    And   I send SC881 request to Azure endpoint
    Then  I can see all the responses are identical for SC881

    Examples:
      | condition            |
      | approve_success      |
      | false_is_recoverable |
