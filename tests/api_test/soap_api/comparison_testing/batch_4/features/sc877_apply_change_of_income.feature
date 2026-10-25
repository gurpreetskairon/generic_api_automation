@SOAP-API
Feature: Comparison Testing - SC877 - Apply Change of Income

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC877 responses are identical


  @positive
  Scenario Outline: Compare SC877 successful transaction response
    Given I create the correct SC877 api payload with different <conditions>
    And   I send the SC877 request to IIB endpoint
    And   I send the SC877 request to Azure endpoint
    Then  I can see all the responses are identical for SC877

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC877 unsuccessful transaction response
    Given I create the correct SC877 api payload with different <conditions>
    And   I send the SC877 request to IIB endpoint
    And   I send the SC877 request to Azure endpoint
    Then  I can see all the responses are identical for SC877

    Examples:
      | conditions               |
      | unsuccessful_transaction |
      | client_not_recognised    |
      | cnp_id_not_recognised    |
