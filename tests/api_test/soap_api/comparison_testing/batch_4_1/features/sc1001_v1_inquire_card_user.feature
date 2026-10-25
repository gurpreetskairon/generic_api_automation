@REST-API
Feature: Comparison Testing - SC1001V1 - Inquire Card User

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC1001 V1 responses are identical


  @positive
  Scenario Outline: Compare SC1001 V1 successful transaction responses
    Given I create the correct SC1001 V1 api payload with different <conditions>
    And   I send the SC1001 V1 request to IIB endpoint
    And   I send the SC1001 V1 request to Azure endpoint
    Then  I can see all the responses are identical for SC1001 V1

    Examples:
      | conditions              |
      | valid_supergold_card    |
      | no_supergold_card       |
      | incorrect_date_of_birth |


  @negative
  Scenario Outline: Compare SC1001 V1 invalid request responses
    Given I create the correct SC1001 V1 api payload with different <conditions>
    And   I send the SC1001 V1 request to IIB endpoint
    And   I send the SC1001 V1 request to Azure endpoint
    Then  I can see all the responses are identical for SC1001 V1

    Examples:
      | conditions            |
      | invalid_client_number |
      | invalid_date_of_birth |
