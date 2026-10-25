@AZURE-SOAP-API @IIB-SOAP-API @SOAP-API @comparison-testing
@sc829-comparison @manageNotification @updateclientnotification
@manageparticipant
Feature: Comparison Testing - SC829 - Manage client notification

  As a consumer of the SC829 SOAP service
  I want to send the same SC829 SOAP request to IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for SC829 business responses

  Acceptance:
  * Azure and IIB responses are identical for the covered SC829 same-payload comparison scenarios.
  * Dynamic 82900 state-changing scenarios validate business outcome equivalence where separate clients are required.

  Execution notes:
  * CMS is the provider for SC829.
  * AIMOS, IMS, WASP, and STAR are consumers that send client notification updates to CMS.
  * Standard comparison scenarios send the same SC829 manageParticipantRequest payload to both IIB and Azure.
  * Detailed validation of result code, result message and subresult message is covered under Azure integration testing.
  * Comparison testing validates that IIB and Azure responses are identical for same-payload scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * XML element ordering is normalized where IIB and Azure return the same values in a different order.
  * LDAP/security authentication scenarios are not included in this comparison feature file.
  * WASP, AIMOS, IMS, and STAR Public Risk Warrant are state-based notifications.
  * For state-based notifications, the first start-date request can return 82900 when the notification is created or activated.
  * Re-running the same start-date request can return 82903 when there is no further update required.
  * Sending an end-date request can return 82900 when the notification is end-dated.
  * Sending an end-date request where no active matching notification exists can return 82903.
  * STAR staff security alert scenarios such as warning letter and trespass order are included because repeated requests are treated as updates and return 82900.
  * BA advised that one representative type code per category is sufficient for the current scope.
  * WAM Profile is not included because BA checked Splunk production logs and no WAM user activity/logs were found for this request.
  * Change of Circumstances is currently out of scope, confirmed by BA.
  * Public Risk Warrant is covered under STAR / STAFFSECURITYALERT / PUBLICRISKWARRANT based on the current confirmed test behaviour.
  * Dynamic 82900 comparison scenarios use separate newly created CMS clients for IIB and Azure because the first endpoint call can create/update the notification and cause the second endpoint to return 82903.
  * Dynamic 82900 scenarios validate business outcome equivalence by comparing result code and message, but do not perform strict same-payload comparison because the client identifiers are different.
  * Jenkins-created dynamic client scenarios are excluded for now because SC829 comparison data is currently managed through the local database.


  @positive @result_code_82900 @successful_response
  Scenario Outline: IIB and Azure return matching successful transaction response for SC829
    Given I create a valid SC829 manageNotification payload for "<consumer_system>" with notification category "<category_code>" and type "<type_code>"
    And   the client exists in CMS
    When  I send the SC829 request to the IIB endpoint
    And   I send the same SC829 request to the Azure endpoint
    Then  I can see the IIB and Azure responses are identical

    Examples:
      | consumer_system | category_code      | type_code |
      | STAR            | STAFFSECURITYALERT | LWAR      |
      | STAR            | STAFFSECURITYALERT | TREP      |


  @positive @result_code_82903 @no_notification_to_update @existing_active_notification
  Scenario Outline: IIB and Azure return matching no notification to update response when notification already exists as active
    Given I create a valid SC829 manageNotification payload for scenario "<scenario_key>"
    And   the client exists in CMS
    And   the same active notification already exists for the client
    When  I send the SC829 request to the IIB endpoint
    And   I send the same SC829 request to the Azure endpoint
    Then  I can see the IIB and Azure responses are identical

    Examples:
      | scenario_key                                 |
      | wasp_existing_start_date                     |
      | aimos_existing_start_date                    |
      | ims_existing_start_date                      |
      | star_public_risk_warrant_existing_start_date |


  @positive @result_code_82903 @no_notification_to_update @end_date_no_active_notification
  Scenario Outline: IIB and Azure return matching no notification to update response when end date is sent but no active notification exists
    Given I create a valid SC829 manageNotification payload for scenario "<scenario_key>"
    And   the client exists in CMS
    And   no active notification exists for the category and type
    And   the payload contains end date "<end_date>" only
    When  I send the SC829 request to the IIB endpoint
    And   I send the same SC829 request to the Azure endpoint
    Then  I can see the IIB and Azure responses are identical

    Examples:
      | scenario_key                                             | end_date             |
      | wasp_end_date_no_active_notification                     | 2026-05-21T12:00:00Z |
      | aimos_end_date_no_active_notification                    | 2026-05-21T12:00:00Z |
      | ims_end_date_no_active_notification                      | 2026-05-21T12:00:00Z |
      | star_public_risk_warrant_end_date_no_active_notification | 2026-05-21T12:00:00Z |


  @negative @result_code_82901 @invalid_request
  Scenario Outline: IIB and Azure return matching invalid request response for SC829
    Given I create an SC829 manageNotification payload with client identifier "<client_identifier>"
    And   the payload contains notification category "<category_code>" and type "<type_code>"
    And   the payload contains start date "<start_date>" and expected end date "<expected_end_date>"
    When  I send the SC829 request to the IIB endpoint
    And   I send the same SC829 request to the Azure endpoint
    Then  I can see the IIB and Azure responses are identical

    Examples:
      | client_identifier | category_code      | type_code    | start_date           | expected_end_date |
      | VALID_CLIENT      | STAFFSECURITYALERT | INVALIDTYPE  | 2026-04-21T12:00:00Z | 2028-04-20        |
      | VALID_CLIENT      | STAFFSECURITYALERT | MISSING_TYPE | 2026-04-21T12:00:00Z | 2028-04-20        |


  @negative @result_code_82902 @client_not_recognised
  Scenario Outline: IIB and Azure return matching client not recognised response for SC829
    Given I create an SC829 manageNotification payload with unrecognised client identifier "<client_identifier>" and identity type "<identity_type>"
    When  I send the SC829 request to the IIB endpoint
    And   I send the same SC829 request to the Azure endpoint
    Then  I can see the IIB and Azure responses are identical

    Examples:
      | client_identifier | identity_type |
      | 555555555         | CLIENTNUMBER  |


  @negative @result_code_82904 @business_validation_failed @invalid_end_date
  Scenario Outline: IIB and Azure return matching transaction unsuccessful response when business validation fails
    Given I create a valid SC829 manageNotification payload for "<consumer_system>" with notification category "<category_code>" and type "<type_code>"
    And   the payload contains start date "<start_date>" and expected end date "<expected_end_date>"
    And   the expected end date is earlier than the start date
    When  I send the SC829 request to the IIB endpoint
    And   I send the same SC829 request to the Azure endpoint
    Then  I can see the IIB and Azure responses are identical

    Examples:
      | consumer_system | category_code      | type_code | start_date           | expected_end_date |
      | STAR            | STAFFSECURITYALERT | TREP      | 2026-04-21T12:00:00Z | 2026-04-20        |


#  @positive @result_code_82900 @successful_response @jenkins_client_creation @dynamic_test_data @business_outcome_comparison
#  Scenario Outline: IIB and Azure return matching successful business outcome using separate Jenkins-created clients
#    Given I retrieve two new CMS clients
#    And   I create a valid SC829 manageNotification payload for "<consumer_system>" using the first Jenkins-created client for IIB with notification category "<category_code>" and type "<type_code>"
#    And   I create a valid SC829 manageNotification payload for "<consumer_system>" using the second Jenkins-created client for Azure with notification category "<category_code>" and type "<type_code>"
#    When  I send the SC829 request to the IIB endpoint using the IIB payload
#    And   I send the SC829 request to the Azure endpoint using the Azure payload
#    Then  I see the result code "<result_code>" returned in both SOAP responses
#    And   I see the result message "<message>" returned in both SOAP responses
#
#    Examples:
#      | consumer_system | category_code      | type_code         | result_code | message                |
#      | WASP            | WARRANTS           | WARRANTTOARREST   | 82900       | Transaction Successful |
#      | AIMOS           | UNDERINVESTIGATION | AIMOS             | 82900       | Transaction Successful |
#      | IMS             | UNDERINVESTIGATION | IMS               | 82900       | Transaction Successful |
#      | STAR            | STAFFSECURITYALERT | PUBLICRISKWARRANT | 82900       | Transaction Successful |
