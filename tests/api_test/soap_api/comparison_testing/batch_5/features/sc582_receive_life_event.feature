@comparison
Feature: Comparison Testing - SC582 - Receive Life Event

  As a client
  I want to send SC582 receive life event requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario: Compare SC582 successful responses between IIB and Azure
    Given I create the SC582 api payload
    When  I send SC582 request to IIB endpoint
    And   I send SC582 request to Azure endpoint
    Then  I can see all the responses are identical for SC582
