@COMPARISON-SOAP-API
@SOAP-API
@sc871-comparison
@participant
Feature: Comparison Testing - SC871 - Manage Client Contact Details

# Notes:
# - Result code 87107 requires a client with an incomplete record in CMS (e.g. a client with no address).
# - Suitable test data is environment-specific and may not be available in all environments.


  Scenario Outline: Compare SC871 successful transaction response
    Given I create the SC871 comparison payload for "<condition>"
    And   I send the SC871 request to IIB endpoint
    And   I send the SC871 request to Azure endpoint
    Then  I can see all the responses are identical for SC871


    Examples:
      | condition                        |
      | update_communication_method_only |


  Scenario Outline: Compare SC871 unsuccessful transaction response
    Given I create the SC871 comparison payload for "<condition>"
    And   I send the SC871 request to IIB endpoint
    And   I send the SC871 request to Azure endpoint
    Then  I can see all the responses are identical for SC871


    Examples:
      | condition                      |
      #| provider_unspecified_condition |
      | invalid_request                |
      | client_not_recognised          |
      | duplicate_or_fraud_client      |
      | duplicate_contact_type         |
      | incomplete_client_record       |
      | user_not_recognised            |
