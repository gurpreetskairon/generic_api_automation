@AZURE-SOAP-API @SOAP-API @sc871-integration
Feature: Azure Integration - SC871 - Manage Client Contact Details

  As a client
  I want to send SOAP requests to the Azure SC871 endpoint
  So that I can validate the response returned for managing client contact details.

  # SC871 supports create, update and delete of client contact details
  # and preferred contact / preferred communication method.
  # Unexpected endpoint/connectivity failure is not covered in automation.

  # Notes:
# - Result code 87107 requires a client with an incomplete record in CMS (e.g. a client with no address).
# - Suitable test data is environment-specific and may not be available in all environments.


  @positive
  Scenario Outline: Check SC871 successful transaction response
    Given I create the correct payload for SC871 with "<condition>"
    When  I send the SC871 request to the Azure endpoint
    Then  I can see the SC871 result code as "<result_code>"
    And   I can see the SC871 result message as "<result_message>"

    Examples:
      | condition                        | result_code | result_message         |
      | update_communication_method_only | 87100       | Transaction Successful |


  @negative
  Scenario Outline: Check SC871 unsuccessful transaction response
    Given I create the payload for SC871 with "<condition>"
    When  I send the SC871 request to the Azure endpoint
    Then  I can see the SC871 result code as "<result_code>"
    And   I can see the SC871 result message as "<result_message>"

    Examples:
      | condition                      | result_code | result_message                                                 |
      #| provider_unspecified_condition | 87101       | Transaction Unsuccessful   ( unable to recreate the scenario )                                    |
      | invalid_request                | 87102       | Invalid request                                                |
      | client_not_recognised          | 87103       | Client not recognised                                          |
      | duplicate_or_fraud_client      | 87104       | Client record is locked for duplicate or fraud                 |
      | duplicate_contact_type         | 87105       | Error – client must have none or only one of each contact type |
      | incomplete_client_record       | 87107       | Client record is incomplete and cannot be published            |
      | user_not_recognised            | 87108       | User not recognised                                            |
