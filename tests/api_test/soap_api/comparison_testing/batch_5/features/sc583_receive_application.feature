@comparison
Feature: Comparison Testing - SC583 - Receive Application

  As a client
  I want to send SC583 receive application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario: Compare SC583 successful responses between IIB and Azure
    Given I create the SC583 api payload
    When  I send SC583 request to IIB endpoint
    And   I send SC583 request to Azure endpoint
    Then  I can see all the responses are identical for SC583
