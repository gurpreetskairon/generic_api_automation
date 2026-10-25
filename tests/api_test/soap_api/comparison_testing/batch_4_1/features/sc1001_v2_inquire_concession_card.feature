@REST-API
Feature: Comparison Testing - SC1001V2 - Inquire Concession Card

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC1001 V2 responses are identical


  @positive
  Scenario Outline: Compare SC1001 V2 successful transaction responses
    Given I create the correct SC1001 V2 api payload with different <conditions>
    And   I send the SC1001 V2 request to IIB endpoint
    And   I send the SC1001 V2 request to Azure endpoint
    Then  I can see all the responses are identical for SC1001 V2

    Examples:
      | conditions                       |
      | community_service_card           |
      | combo_card                       |
      | veteran_combo_card               |
      | supergold_without_valid_csc      |
      | no_csc_card                      |
      | incorrect_date_of_birth          |
      | client_not_found                 |
      | client_number_with_leading_zeros |


  @negative
  Scenario Outline: Compare SC1001 V2 invalid request responses
    Given I create the correct SC1001 V2 api payload with different <conditions>
    And   I send the SC1001 V2 request to IIB endpoint
    And   I send the SC1001 V2 request to Azure endpoint
    Then  I can see all the responses are identical for SC1001 V2

    Examples:
      | conditions      |
      | invalid_request |
