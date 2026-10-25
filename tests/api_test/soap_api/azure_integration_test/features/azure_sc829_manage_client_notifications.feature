@AZURE-SOAP-API @SOAP-API @sc829-integration
@manageNotification
@updateclientnotification
@manageparticipant
Feature: Azure Integration - SC829 - Manage client notification

  As a consumer of the SC829 SOAP service
  I want to send client notification updates to CMS through the Azure endpoint
  So that CMS can create, update, end-date, or identify client notifications according to the business rules

  Acceptance:
  * 82900 - Transaction Successful
  * 82901 - Invalid request
  * 82902 - Client not recognised
  * 82903 - No notification to update
  * 82904 - Transaction Unsuccessful
  * The service updates the following supported client notifications:
    (1) Warrant to arrest / public risk warrant
    (2) AIMOS Under Investigation
    (3) IMS Under Investigation
    (4) STAR special caution
  * A valid SC829 request must include:
    (1) client identifier
    (2) category code
    (3) type code
    (4) required date information for the requested action
    (5) recognised category and type code hierarchy
    (6) recognised client record in CMS

  Execution notes:
  * CMS is the provider for SC829.
  * AIMOS, IMS, WASP, and STAR are consumers that send client notification updates to CMS.
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


  @positive @result_code_82900
  Scenario Outline: CMS updates the client notification successfully
    Given I create a valid SC829 manageNotification payload for "<consumer_system>" with notification category "<category_code>" and type "<type_code>"
    And   the client exists in CMS
    When  I send the SC829 request to the endpoint
    Then  I can see the "Transaction Successful" response returned
    And   I see the result code "<result_code>" returned in the response SOAP
    And   I see the result message "<message>" returned in the response SOAP

    Examples:
      | consumer_system | category_code      | type_code | result_code | message                |
      | STAR            | STAFFSECURITYALERT | LWAR      | 82900       | Transaction Successful |
      | STAR            | STAFFSECURITYALERT | TREP      | 82900       | Transaction Successful |


  @positive @result_code_82903 @no_notification_to_update @existing_active_notification
  Scenario Outline: CMS returns no notification to update when the notification already exists as active
    Given I create a valid SC829 manageNotification payload for scenario "<scenario_key>"
    And   the client exists in CMS
    And   the same active notification already exists for the client
    When  I send the SC829 request to the endpoint
    Then  I can see the SOAP response returned
    And   I see the result code "<result_code>" returned in the response SOAP
    And   I see the result message "<message>" returned in the response SOAP
    And   I see the subresult message contains "<subresult_message>"

    Examples:
      | scenario_key                                 | result_code | message                   | subresult_message                    |
      | wasp_existing_start_date                     | 82903       | No notification to update | MSDSCSC13- already existed as active |
      | aimos_existing_start_date                    | 82903       | No notification to update | MSDSCSC15- already existed as active |
      | ims_existing_start_date                      | 82903       | No notification to update | MSDSCSC16- already existed as active |
      | star_public_risk_warrant_existing_start_date | 82903       | No notification to update | MSDSCSC14- already existed as active |


  @positive @result_code_82903 @no_notification_to_update @end_date_no_active_notification
  Scenario Outline: CMS returns no notification to update when end date is sent but no active notification exists
    Given I create a valid SC829 manageNotification payload for scenario "<scenario_key>"
    And   the client exists in CMS
    And   no active notification exists for the category and type
    And   the payload contains end date "<end_date>" only
    When  I send the SC829 request to the endpoint
    Then  I can see the SOAP response returned
    And   I see the result code "<result_code>" returned in the response SOAP
    And   I see the result message "<message>" returned in the response SOAP
    And   I see the subresult message contains "<subresult_message>"

    Examples:
      | scenario_key                                             | end_date             | result_code | message                   | subresult_message                             |
      | wasp_end_date_no_active_notification                     | 2026-05-21T12:00:00Z | 82903       | No notification to update | You entered the end date for the notification |
      | aimos_end_date_no_active_notification                    | 2026-05-21T12:00:00Z | 82903       | No notification to update | You entered the end date for the notification |
      | ims_end_date_no_active_notification                      | 2026-05-21T12:00:00Z | 82903       | No notification to update | You entered the end date for the notification |
      | star_public_risk_warrant_end_date_no_active_notification | 2026-05-21T12:00:00Z | 82903       | No notification to update | You entered the end date for the notification |


  @negative @result_code_82901 @invalid_request
  Scenario Outline: CMS returns invalid request when request-level details are invalid
    Given I create an SC829 manageNotification payload with client identifier "<client_identifier>"
    And   the payload contains notification category "<category_code>" and type "<type_code>"
    And   the payload contains start date "<start_date>" and expected end date "<expected_end_date>"
    When  I send the SC829 request to the endpoint
    Then  I can see the SOAP response returned
    And   I see the result code "<result_code>" returned in the response SOAP
    And   I see the subresult message contains "<subresult_message>"

    Examples:
      | client_identifier | category_code      | type_code    | start_date           | expected_end_date | result_code | subresult_message                       |
      | VALID_CLIENT      | STAFFSECURITYALERT | INVALIDTYPE  | 2026-04-21T12:00:00Z | 2028-04-20        | 82901       | Notification type not recognised        |
      | VALID_CLIENT      | STAFFSECURITYALERT | MISSING_TYPE | 2026-04-21T12:00:00Z | 2028-04-20        | 82901       | At least one mandatory field is missing |


  @negative @result_code_82902 @client_not_recognised
  Scenario Outline: CMS returns client not recognised when the client identifier does not exist in CMS
    Given I create an SC829 manageNotification payload with unrecognised client identifier "<client_identifier>" and identity type "<identity_type>"
    When  I send the SC829 request to the endpoint
    Then  I can see the SOAP response returned
    And   I see the result code "<result_code>" returned in the response SOAP
    And   I see the result message "<message>" returned in the response SOAP

    Examples:
      | client_identifier | identity_type | result_code | message               |
      | 555555555         | CLIENTNUMBER  | 82902       | Client not recognised |


  @negative @result_code_82904 @business_validation_failed
  Scenario Outline: CMS returns transaction unsuccessful when CMS business validation fails
    Given I create a valid SC829 manageNotification payload for "<consumer_system>" with notification category "<category_code>" and type "<type_code>"
    And   the payload contains start date "<start_date>" and expected end date "<expected_end_date>"
    And   the expected end date is earlier than the start date
    When  I send the SC829 request to the endpoint
    Then  I can see the SOAP response returned
    And   I see the result code "<result_code>" returned in the response SOAP
    And   I see the result message "<message>" returned in the response SOAP

    Examples:
      | consumer_system | category_code      | type_code | start_date           | expected_end_date | result_code | message                  |
      | STAR            | STAFFSECURITYALERT | TREP      | 2026-04-21T12:00:00Z | 2026-04-20        | 82904       | Transaction Unsuccessful |


  @positive @result_code_82900 @successful_response @jenkins_client_creation @dynamic_test_data
  Scenario Outline: CMS creates notification successfully using a newly created Jenkins client
    Given I retrieve a new CMS clients
    And   I create a valid SC829 manageNotification payload for "<consumer_system>" using the Jenkins-created client with notification category "<category_code>" and type "<type_code>"
    When  I send the SC829 request to the endpoint
    Then  I can see the "Transaction Successful" response returned
    And   I see the result code "<result_code>" returned in the response SOAP
    And   I see the result message "<message>" returned in the response SOAP

    Examples:
      | consumer_system | category_code      | type_code         | result_code | message                |
      | WASP            | WARRANTS           | WARRANTTOARREST   | 82900       | Transaction Successful |
      | AIMOS           | UNDERINVESTIGATION | AIMOS             | 82900       | Transaction Successful |
      | IMS             | UNDERINVESTIGATION | IMS               | 82900       | Transaction Successful |
      | STAR            | STAFFSECURITYALERT | PUBLICRISKWARRANT | 82900       | Transaction Successful |
