@IIB-AZURE-COMPARISON @SOAP-API @sc557-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC557v2 - Inquire ongoing assistance

  As a client
  I want to compare the responses from the IIB and Azure for SC557
  So that I can see whether the responses are identical

Notes:


  @positive
  Scenario Outline: Compare SC557v2 successful response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions             |
      | transaction_successful |


  @negative
  Scenario Outline: Compare SC557v2 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions      |
      | no_payment_card |
#    | card_not_allocated_any_client      |
#    | card_not_allocated_specific_client |
#    | card_number_not_recognised         |
#    | xml_validation_failure             |
