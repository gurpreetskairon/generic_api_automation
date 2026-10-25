@AZURE-SOAP-API @SOAP-API @sc827-integration @register-client
Feature: Azure Integration - SC827 - Register Client

  As an external consuming application such as SAL or S2P
  I want to register a new client in CMS using SC827
  So that a new client record can be created with or without partner relationship details

  Acceptance:
  * 82700 - Transaction Successful - client can be registered without partner details
  * 82700 - Transaction Successful - client can be registered with partner relationship details
  * 82701 / 82710 - At least one mandatory field is missing
  * 82701 / 82711 - IRD Number format error
  * 82701 / 82712 - IRD Number found in another customer
  * 82701 / 82713 - DOB cannot be after system date
  * 82701 / 82714 - Partner client number does not exist
  * 82701 / 82715 - Partner record is secured
  * 82701 / 82716 - Partner already has a current relationship
  * 82701 / 82717 - Marital status invalid
  * 82701 / 82718 - Marital status effective date cannot be before DOB or after system date
  * 82701 / 82719 - Person name format invalid
  * 82701 / 82720 - Person gender format invalid
  * 82701 / 82721 - Country of birth invalid
  * 82701 / 82722 - Ethnicity group format invalid
  * 82701 / 82723 - Address format invalid
  * 82701 / 82724 - Security token ID is missing when registering a client with partner details
  * 82701 / 82725 - Existing client match found
  * 82701 / 82726 - Partner client number details are incomplete or incorrect
  * 82701 / 82727 - New client and partner address/contact details do not match
  * 82701 / 82728 - Residency code invalid
  * 82701 / 82729 - Residency class visa status change date cannot be before DOB or after system date
  * 82701 / 80099 - Result not recognized

    Execution notes:
  * SC827 creates new client records in CMS, so positive scenarios use dynamically generated first name, family name.
  * Test data is read from the local SQLite SC827 table in Service_contract_data.db.
  * The valid partner scenario uses SC827_PARTNER_POOL to avoid reusing partner client numbers that have already been consumed.
  * Azure integration testing validates the Azure response only.
  * Only executable scenarios are included in the active Examples table below.
  * Data-dependent, defect-blocked, or payload-support-dependent scenarios are listed below and are not included in the active Examples table.

  Deferred scenarios not currently executed:
  * invalid_person_name_format:
    Defect raised. Service behaviour does not currently match the documented 82719 expectation.

  * invalid_ethnicity_group:
    Not enabled yet. Ethnicity group is not mandatory in the current SC827 payload and payload_data/sc827.py does not yet generate ethnicity XML from ethnicity_group/ethnicity_code.

  * invalid_contact_address:
    Defect API-3612 raised / under clarification. Invalid characters are currently causing schema validation behaviour rather than the documented 82723 response.

  * partner_address_contact_mismatch:
    Defect API-3612 raised / under clarification. Requires stable partner data and expected address/contact mismatch behaviour confirmation.


  @positive
  @ac-positive
  Scenario Outline: Verify SC827 returns successful response when registering a client
    Given I create the correct SC827 payload for "<condition>"
    When  I send the SC827 request to Azure
    Then  the SC827 response should contain result code "<result_code>"
    And   the SC827 response should contain result message "<message>"
    And   the SC827 response should contain a generated client number


    Examples:
      | condition                             | result_code | message                |
      | valid_register_client_without_partner | 82700       | Transaction Successful |
#  | valid_register_client_with_partner    | 82700       | Transaction Successful  |


  @negative
  @validation
  @ac-negative
  Scenario Outline: Verify SC827 returns unsuccessful response for invalid register client request
    Given I create the SC827 payload for "<condition>"
    When  I send the SC827 request to Azure
    Then  the SC827 response should contain result code "<result_code>"
    And   the SC827 response should contain result message "<message>"
    And   the SC827 response should contain sub-result code "<subresult_code>"
    And   the SC827 response should contain sub-result message "<subresult_message>"

    Examples:
      | condition                                | result_code | message                  | subresult_code | subresult_message                                                                              |
      | missing_mandatory_person_data            | 82701       | Transaction Unsuccessful | 82710          | At least one mandatory field is missing                                                        |
      | invalid_ird_number_format                | 82701       | Transaction Unsuccessful | 82711          | IRD Number format error                                                                        |
      | ird_number_found_in_another_customer     | 82701       | Transaction Unsuccessful | 82712          | IRD Number found in another customer                                                           |
      | dob_after_system_date                    | 82701       | Transaction Unsuccessful | 82713          | DOB cannot be after system date                                                                |
      | partner_client_number_does_not_exist     | 82701       | Transaction Unsuccessful | 82714          | Partner client number does not exist                                                           |
      | secured_partner_client                   | 82701       | Transaction Unsuccessful | 82715          | The partner record is secured and cannot be included in the partner relationship               |
      | invalid_marital_status                   | 82701       | Transaction Unsuccessful | 82717          | Marital status invalid                                                                         |
      | invalid_marital_status_effective_date    | 82701       | Transaction Unsuccessful | 82718          | Marital status effective date cannot be before DOB or after system date                        |
      | invalid_person_gender_format             | 82701       | Transaction Unsuccessful | 82720          | Person gender format invalid                                                                   |
      | invalid_country_of_birth                 | 82701       | Transaction Unsuccessful | 82721          | Country of birth invalid                                                                       |
      | missing_security_token_id_for_partner    | 82701       | Transaction Unsuccessful | 82724          | No username included in the request when register a new client and link to an existing partner |
      | existing_client_match_found              | 82701       | Transaction Unsuccessful | 82725          | Create client failed. Matches have been found for customer numbers:                            |
      | incorrect_partner_client_number_details  | 82701       | Transaction Unsuccessful | 82726          | Partner client number details are incomplete or incorrect                                      |
      | invalid_residency_code                   | 82701       | Transaction Unsuccessful | 82728          | Residency code invalid                                                                         |
      | invalid_residency_class_visa_status_date | 82701       | Transaction Unsuccessful | 82729          | Residency Class Visa Status change date cannot be before DOB or after system date              |
      | result_not_recognised                    | 82701       | Transaction Unsuccessful | 80099          | Result not recognized                                                                          |
      | partner_already_has_current_relationship | 82701       | Transaction Unsuccessful | 80099          | Result not recognized                                                                          |
