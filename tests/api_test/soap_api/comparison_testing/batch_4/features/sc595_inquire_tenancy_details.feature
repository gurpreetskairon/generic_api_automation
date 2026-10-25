@comparison
Feature: Comparison Testing - SC595 - Inquire Tenancy Details

  As a client
  I want to send SC595 Inquire Tenancy Details requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC595 successful responses between IIB and Azure
    Given I create the SC595 api payload for <condition>
    When  I send the SC595 request to IIB endpoint
    And   I send the SC595 request to Azure endpoint
    Then  I can see all the responses are identical for SC595

    Examples:
      | condition              |
      | transaction_successful |
      | client_not_recognised  |
      | no_services            |
