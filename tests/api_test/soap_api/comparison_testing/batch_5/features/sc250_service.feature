@comparison
Feature: Comparison Testing - SC250 - Register Supplier

  As a client
  I want to send SC250 register supplier requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario: Compare SC250 successful responses between IIB and Azure
    Given I create the SC250 api payload
    When  I send SC250 request to IIB endpoint
    And   I send SC250 request to Azure endpoint
    Then  I can see all the responses are identical for SC250
