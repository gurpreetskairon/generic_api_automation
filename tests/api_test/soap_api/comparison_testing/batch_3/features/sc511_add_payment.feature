@comparison
Feature: Comparison Testing - SC511 - Add Payment

  As a client
  I want to send SC511 add payment requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC511 successful responses between IIB and Azure
    Given I create the SC511 api payload for <condition>
    When  I send SC511 request to IIB endpoint
    And   I send SC511 request to Azure endpoint
    Then  I can see all the responses are identical for SC511

    Examples:
      | condition              |
      | transaction_successful |


  @negative
  Scenario Outline: Compare SC511 negative responses between IIB and Azure
    Given I create the SC511 api payload for <condition>
    When  I send SC511 request to IIB endpoint
    And   I send SC511 request to Azure endpoint
    Then  I can see all the responses are identical for SC511

    Examples:
      | condition                               |
      | payment_expiry_greater_than_card_expiry |
      | max_active_payments                     |
      | total_value_limit                       |
      | activate_unallocated_card               |
      | unknown_client_number                   |
      | xml_validation                          |
      | payment_does_not_exist                  |
      | same_card_number                        |
      | transfer_and_update_concurrently        |
      | unknown_card_number                     |
      | existing_payment                        |
