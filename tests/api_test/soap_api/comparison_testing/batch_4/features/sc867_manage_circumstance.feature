@comparison
Feature: Comparison Testing - SC867 - Manage Circumstance

  As a client
  I want to send SC867 manage circumstance requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC867 successful responses between IIB and Azure
    Given I create the SC867 api payload for <condition>
    When  I send SC867 request to IIB endpoint
    And   I send SC867 request to Azure endpoint
    Then  I can see all the responses are identical for SC867

    Examples:
      | condition                |
      | transaction_successful   |
      | duplicate_med_cert       |
      | transaction_unsuccessful |


  @negative
  Scenario Outline: Compare SC867 successful responses between IIB and Azure for negative scenarios
    Given I create the SC867 api payload for <condition>
    When  I send SC867 request to IIB endpoint
    And   I send SC867 request to Azure endpoint
    Then  I can see all the responses are identical for SC867

    Examples:
      | condition           |
      | user_not_recognised |
