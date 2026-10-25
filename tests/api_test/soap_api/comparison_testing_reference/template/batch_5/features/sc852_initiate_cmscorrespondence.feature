@comparison
Feature: Comparison Testing - SC852 - Initiate Cmscorrespondence

  As a client
  I want to send SC852 initiate cmscorrespondence requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC852 successful responses between IIB and Azure
    Given I create the SC852 api payload for <condition>
    When  I send SC852 request to IIB endpoint
    And   I send SC852 request to Azure endpoint
    Then  I can see all the responses are identical for SC852

    Examples:
      | condition           |
      | successful_response |
