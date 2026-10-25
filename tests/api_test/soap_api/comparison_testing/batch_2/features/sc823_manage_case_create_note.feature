@AZURE-SOAP-API @SOAP-API @sc823-comparison @manage-case @create-unstructured-note
Feature: Comparison Testing - SC823 - Manage Case Create Unstructured Note

  As an API consumer
  I want to send the same SC823 Manage Case request to IIB and Azure
  So that I can confirm both systems return identical SOAP response bodies

  The comparison ignores XML namespace-prefix differences.
  XML element order may be ignored where it does not affect the business response.
  Detailed business result-code and message validation is handled separately.
  The same payload, transaction ID, audit ID and request date-time are reused
  for both the IIB and Azure requests.

    Acceptance:
  * Azure and IIB responses should be identical for the covered SC823 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * A successful request returns result code 82300 and message Transaction Successful.
  * An unsuccessful transaction returns result code 82301 and message Transaction Unsuccessful. The response may also contain provider sub-results.
  * An unrecognised user returns result code 82309 and message User not recognised.
  * A client number that does not identify a CMS client returns result code 82310 and message Client not recognised.
  * An invalid request returns result code 82311 and message Invalid request.
  * Invalid-request coverage includes:
    - A client with no CaseEvent.
    - An invalid action or operation value.
    - An invalid CaseEvent type code.
    - Note text longer than 4000 characters.
    - Note text containing unsupported special characters.
    - A short description longer than 100 characters.
  * A client locked for duplicate or fraud returns result code 82312 and message Client record is locked for duplicate or fraud.

  Execution notes:
  * The same SC823 payload is sent to both IIB and Azure for each comparison scenario.
  * transaction unsuccessful scenario has been excluded from script based on BA's comment on the story -  no logs for the scenario in any of the environment
  * The successful scenario uses operation CREATECASEEVENTANDNOTE with a recognised CaseEvent type and note type.
  * The Declare Income request uses CaseEvent type DSS525 and note subject type COMT.
  * The note text must not exceed 4000 characters, and the short description must not exceed 100 characters.
  * Secured clients and clients with notifications can still have a note created.


  @positive
  Scenario Outline: Compare SC823 transaction responses between IIB and Azure
    Given I create the SC823 api payload for <condition>
    When  I send SC823 request to IIB endpoint
    And   I send SC823 request to Azure endpoint
    Then  I can see all the responses are identical for SC823

    Examples:
      | condition                |
      | successful_response      |
      | append_to_existing_note  |
      | update_case_event_status |


  @negative @authentication
  Scenario: Compare SC823 response for an unrecognised user
    Given I create the SC823 api payload for user_not_recognised
    When  I send SC823 request to IIB endpoint
    And   I send SC823 request to Azure endpoint
    Then  I can see all the responses are identical for SC823


  @negative @client-validation
  Scenario Outline: Compare SC823 client validation responses between IIB and Azure
    Given I create the SC823 api payload for <condition>
    When  I send SC823 request to IIB endpoint
    And   I send SC823 request to Azure endpoint
    Then  I can see all the responses are identical for SC823

    Examples:
      | condition                   |
      | client_not_recognised       |
      | client_locked_for_duplicate |
      | client_locked_for_fraud     |


  @negative @invalid-request
  Scenario Outline: Compare SC823 invalid request responses between IIB and Azure
    Given I create the SC823 api payload for <condition>
    When  I send SC823 request to IIB endpoint
    And   I send SC823 request to Azure endpoint
    Then  I can see all the responses are identical for SC823

    Examples:
      | condition                                 |
      | invalid_request_client_without_case_event |
      | invalid_action                            |
      | invalid_case_event_type                   |
      | note_text_over_4000_characters            |
      | note_text_with_special_characters         |
      | short_description_over_100_characters     |
      | short_description_with_special_characters |
