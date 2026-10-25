@comparison
Feature: Comparison Testing - SC820 - Calculate Back Dated Review

  As a client
  I want to send SC820 calculate back dated review requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC820 successful responses between IIB and Azure
    Given I create the SC820 api payload for <condition>
    When  I send SC820 request to IIB endpoint
    And   I send SC820 request to Azure endpoint
    Then  I can see all the responses are identical for SC820

    Examples:
      | condition               |
      | transaction_successful  |
      | transaction_unsuccessful|
