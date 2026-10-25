@comparison
Feature: Comparison Testing - SC821 - Assess Processing Review

  As a client
  I want to send SC821 assess processing review requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC821 successful responses between IIB and Azure
    Given I create the SC821 api payload for <condition>
    When  I send SC821 request to IIB endpoint
    And   I send SC821 request to Azure endpoint
    Then  I can see all the responses are identical for SC821

    Examples:
      | condition              |
      | transaction_successful |
