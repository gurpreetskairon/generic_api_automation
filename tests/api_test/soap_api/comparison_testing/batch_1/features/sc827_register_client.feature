@AZURE-SOAP-API @SOAP-API @sc827-comparison
@registerclient
Feature: Comparison Testing - SC827 - Register Client

  As a consumer of the SC827 SOAP service
  I want to compare the SC827 response between Azure and IIB
  So that I can confirm Azure behaves like-for-like with IIB for the agreed Register Client scenarios

  Acceptance:
  * 82700 - Transaction Successful
  * 82701 - Transaction Unsuccessful
  * 82710 - At least one mandatory field is missing
  * 82711 - IRD Number format error
  * 82712 - IRD Number found in another customer
  * 82713 - DOB cannot be after system date
  * 82714 - Partner client number does not exist
  * 82715 - The partner record is secured and cannot be included in the partner relationship
  * 82716 - Client details cannot be saved. The partner selected has an existing partner relationship
  * 82717 - Marital status invalid
  * 82718 - Marital status effective date cannot be before DOB or after system date
  * 82719 - Person name format invalid. Family Name and First Name are mandatory.
  * 82720 - Person gender format invalid
  * 82721 - Country of birth invalid
  * 82722 - Ethnicity group format invalid
  * 82723 - Address format invalid
  * 82724 - No username included in the request when register a new client and link to an existing partner
  * 82725 - Create client failed. Matches have been found for customer numbers:
  * 82726 - Partner client number details are incomplete or incorrect
  * 82727 - There was a mismatch between new client and partner address/contact details
  * 82728 - Residency code invalid
  * 82729 - Residency Class Visa Status change date cannot be before DOB or after system date
  * 80099 - Result not recognized

  Execution notes:
  * SC827 is a state-changing service and creates new client records in CMS.
  * Test data is read from the local SQLite SC827 table in Service_contract_data.db.
  * Step definitions should not hardcode test data.
  * Positive scenarios use dynamically generated first name, family name, auditId, transactionId and requestDateTime.
  * Generated client numbers are not expected to match between Azure and IIB because each endpoint may create a separate client record.
  * XML namespace prefixes are not treated as business-data differences.
  * Azure-vs-IIB comparison validates result code, result message, sub-result code and sub-result message.
  * Data-dependent, defect-blocked, or payload-support-dependent scenarios are listed below and are not included in the active Examples table.
  * SC827 is not validated using full identical response comparison because it is a state-changing create-client service.
    Azure and IIB can generate separate client records and dynamic values for the same business condition.
    Therefore, comparison testing validates the agreed business outcome fields: result code, result message,
    sub-result code and sub-result message. Generated client numbers are checked for presence only and are not expected to match.

  Deferred scenarios not currently executed:

  * invalid_person_name_format:
    Defect raised. Service behaviour does not currently match the documented 82719 expectation.
  * invalid_ethnicity_group:
    Not enabled yet. Ethnicity group is not mandatory in the current SC827 payload and payload_data/sc827.py does not yet generate ethnicity XML from ethnicity_group/ethnicity_code.
  * invalid_contact_address:
    Defect API-3612 raised / under clarification. Invalid characters are currently causing schema validation behaviour rather than the documented 82723 response.
  * partner_address_contact_mismatch:
    Defect API-3612 raised / under clarification. Requires stable partner data and expected address/contact mismatch behaviour confirmation.
  * SC827 is state-changing. For positive create-client scenarios, Azure and IIB do not use the exact same request payload.
    Two equivalent payloads are generated for the same condition so that the first endpoint does not create a client
    that causes the second endpoint to fail with an existing-client match.
  * For negative scenarios, the same payload can be sent to both Azure and IIB where the request does not create a client.


  @positive
  @result_code_82700
  @successful_response
  Scenario Outline: Compare SC827 successful Register Client response between Azure and IIB
    Given I create the correct SC827 comparison payload for "<condition>"
    When  I send the SC827 request to both Azure and IIB endpoints
    Then  I can see the responses are identical


    Examples:
      | condition                             |
      | valid_register_client_without_partner |
      | valid_register_client_with_partner    |


  @negative
  @validation
  @result_code_82701
  @transaction_unsuccessful
  Scenario Outline: Compare SC827 unsuccessful Register Client response between Azure and IIB
    Given I create the SC827 comparison payload for "<condition>"
    When  I send the SC827 request to both Azure and IIB endpoints
    Then  I can see the responses are identical


    Examples:
      | condition                                |
      | missing_mandatory_person_data            |
      | invalid_ird_number_format                |
      | ird_number_found_in_another_customer     |
      | dob_after_system_date                    |
      | partner_client_number_does_not_exist     |
      | secured_partner_client                   |
      | invalid_marital_status                   |
      | invalid_marital_status_effective_date    |
      | invalid_person_gender_format             |
      | invalid_country_of_birth                 |
      | missing_security_token_id_for_partner    |
      | existing_client_match_found              |
      | incorrect_partner_client_number_details  |
      | invalid_residency_code                   |
      | invalid_residency_class_visa_status_date |
      | result_not_recognised                    |
      | partner_already_has_current_relationship |
