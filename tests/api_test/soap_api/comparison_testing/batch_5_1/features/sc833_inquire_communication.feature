@comparison
Feature: Comparison Testing - SC833 - Inquire Communication

  As a client
  I want to send SC833 inquire communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC833 successful responses between IIB and Azure
    Given I create the SC833 api payload for <condition>
    When  I send SC833 request to IIB endpoint
    And   I send SC833 request to Azure endpoint
    Then  I can see all the responses are identical for SC833

    Examples:
      | condition                    |
      | transaction_successful       |
      | no_current_notification      |
