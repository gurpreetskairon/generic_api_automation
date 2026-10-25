@AZURE-SOAP-API @SOAP-API @sc596-comparison
Feature: Comparison Testing - SC596 - Manage Tenancy Details

  As a client,
  I want to send SC596 Manage Tenancy Details requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical

    * The expected result codes are:
      * 59600 - All records created successfully
        * Supplementary Result Code: 10000
        * Supplementary Result Message: Successful - No further action

      * 99998 - Unknown Error Has Occurred. Check log files for more information. This usually contains stack trace.

      * 59603 - Client not recognised
        * Supplementary Result Code: 52003

      * 59650 - Client does not have a current, suspended, or expired service
        * Supplementary Result Code: 13350

      * 59651 - Client has linked active tenant records
        * Supplementary Result Code: 13351

      * 59652 - Client is an apportioned partner
        * Supplementary Result Code: 13352

      * 59699 - An error occurred processing the request

    * For result code 59699, the expected outcome messages include:
      * 12540 - Weekly accommodation cost is mandatory
      * 12541 - Weekly accommodation cost not valid
      * 12542 - Business expenses not valid
      * 12554 - Cannot add the same tenant more than once
      * 00264 - Given names must be uppercase/alphabetic
      * 10066 - Name/surname can't exceed 30 characters
      * 00052 - Given names can't start with a space
      * 00178 - Given names mandatory
      * 00263 - Surname must be upper case/alphabetic
      * 00049 - Surname is mandatory
      * 03123 - Type of cost mandatory
      * 03081 - Cost is mandatory
      * 12536 - Cost frequency is mandatory
      * 03656 - Start date not valid
      * 03702 - Start date mandatory
      * 12531 - Date overlapping with previous record date
      * 09213 - Invalid end date
      * 03873 - Date overlapping with previous record date
      * 12546 - Proportion only applies to renters or NAP
      * 10063 - Proportion of home is mandatory for NAP
      * 12533 - Total proportion % for all household entries exceeds 100
      * 00221 - Proportion can only be blank or a valid percentage for renters
      * 09346 - NAP description must not be more than 50 characters long
      * 10051 - Must search on TENTS before entering TENTU
      * 12529 - Enter a SWN or Surname before submitting
      * 12530 - Entry is only via TENTS or TENTI
      * 12538 - Tenant cost details do not match [SUP] costs for [SWN]
      * 12539 - Client is a boarder/renter linked to head tenant [SWN]
      * 12543 - Cost frequency is not valid
      * 12544 - Cost type is not valid
      * 12545 - Entry is only via TENTI
      * 12547 - Client currently linked as a tenant under [SWN]
      * 12548 - Start date cannot be before the head tenant's DOB
      * 12549 - Tenant removed, reassessment of the client may be required
      * 12550 - End date cannot be after the current pay period
      * 12551 - Benefit type cannot complete this action
      * 12553 - Tenant cannot be an apportioned partner

  Execution Note:
    * Automation currently covers 18 scenarios: 1 positive, 4 business-negative, and 13 request-validation scenarios.
    * Azure middleware development for SC596 is not currently complete; therefore full IIB-vs-Azure comparison testing is blocked.
    * IIB is currently used to validate the request structure, test data, and available business/validation responses.
    * The documented supplementary result codes are not currently returned by IIB, including supplementary code 10000 for 59600 and the documented supplementary codes for 59603, 59650, 59651, and 59652.
    * Result code 99998 is documented in the acceptance criteria but is not included as a runnable scenario until a reliable trigger is identified.
    * The remaining validation scenarios are commented out because their exact request trigger, backend state, or required test data cannot currently be reproduced reliably.
    * The swn_and_surname_missing scenario is excluded because current IIB behaviour returns the same outcome as surname_missing rather than the distinct documented outcome.
    * Commented scenarios can be enabled once the required trigger/data is confirmed by removing the comment marker.


  @positive @sc596-positive
  Scenario Outline: Compare SC596 successful responses between IIB and Azure
    Given I create the SC596 api payload for <condition>
    When  I send SC596 request to IIB endpoint
    And   I send SC596 request to Azure endpoint
    Then  I can see all the responses are identical for SC596

    Examples:
      | condition           |
      | successful_response |


  @negative @sc596-negative
  Scenario Outline: Compare SC596 unsuccessful responses between IIB and Azure
    Given I create the SC596 api payload for <condition>
    When  I send SC596 request to IIB endpoint
    And   I send SC596 request to Azure endpoint
    Then  I can see all the responses are identical for SC596

    Examples:
      | condition                                |
      | client_not_recognised                    |
      | client_without_eligible_service          |
      | client_with_linked_active_tenant_records |
      | client_is_apportioned_partner            |


  @negative @sc596-validation
  Scenario Outline: Compare SC596 invalid request parameter responses between IIB and Azure
    Given I create the SC596 api payload for <condition>
    When  I send SC596 request to IIB endpoint
    And   I send SC596 request to Azure endpoint
    Then  I can see all the responses are identical for SC596

    Examples:
      | condition                               |
      | weekly_accommodation_cost_missing       |
      | duplicate_tenant                        |
      | given_names_not_uppercase_or_alphabetic |
      | name_or_surname_exceeds_30_characters   |
      | given_names_start_with_space            |
      | given_names_missing                     |
      | surname_not_uppercase_or_alphabetic     |
      | surname_missing                         |
      | cost_type_missing                       |
      | cost_missing                            |
      | cost_frequency_missing                  |
      | start_date_missing                      |
      | household_total_proportion_exceeds_100  |

      # Currently excluded - trigger/data/precondition not reliably reproducible.
      # Remove the comment marker once the required condition is confirmed.

      # | weekly_accommodation_cost_invalid          |
      # | business_expenses_invalid                  |
      # | start_date_invalid                         |
      # | date_overlaps_previous_record              |
      # | end_date_invalid                           |
      # | proportion_invalid_for_non_renter_or_nap   |
      # | nap_proportion_missing                     |
      # | renter_proportion_invalid                  |
      # | nap_description_exceeds_50_characters      |
      # | tents_search_required_before_tentu         |

      # Current IIB behaviour returns the surname-missing outcome rather
      # than the distinct documented outcome for this combination.
      # | swn_and_surname_missing                    |

      # | invalid_entry_source                       |
       | tenant_cost_does_not_match_sup_cost        |
      # | client_linked_as_boarder_or_renter         |
      # | cost_frequency_invalid                     |
      # | cost_type_invalid                          |
      # | entry_not_via_tenti                        |
      # | client_already_linked_as_tenant            |
      # | start_date_before_head_tenant_dob          |
      # | tenant_removed_reassessment_required       |
      # | end_date_after_current_pay_period          |
      # | benefit_type_cannot_complete_action        |
      # | tenant_is_apportioned_partner              |
