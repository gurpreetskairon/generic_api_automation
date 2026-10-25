@comparison
Feature: Comparison Testing - DP863 - manage client appointment booking

  As a client
  I want to send DP863 manage client appointment bookings to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical

  NOTES:
  Dates/Times cannot be reused, it needs to either be unique everytime or the initial appointment
  needs to be cancelled first before the same timeslot can be booked again

  The positive scenarios with request value "reschedule_appointment" and "cancel_appointment" rely
  on data from the DB that is updated everytime the "new_appointment" scenario is run. when its run
  it will update 2 DB entries. e.g the "new_appointment" scenario will create the data required for the
  other 2 positive scenarios.
  * DB entry with condition "reschedule_appointment" will have the booking_start_time &
    booking_end_time updated with what was used in the "new_appointment" to help
    determine what timeslot to not use when rescheduling.
  * DB entry with condition "cancel_appointment" will have the booking_ID updated which will then
    be used with the "cancel_appointment" scenario to delete the booked appointment.
  * script flow will likely need updating once azure is up and running since Dates/Times cannot be resued



  @positive
  Scenario Outline: Compare DP863 successful responses between IIB and Azure
    Given I create the DP863 api <request> payload for <condition>
    When  I send DP863 request to IIB endpoint
    And   I send DP863 request to Azure endpoint
    Then  I can see all the responses are identical for DP863

    Examples:
      | condition           | request                |
      | successful_response | new_appointment        |
      | successful_response | reschedule_appointment |
      | successful_response | cancel_appointment     |


  @negative
  Scenario Outline: Compare DP863 delete appointment negative responses between IIB and Azure
    Given I create the DP863 api <request> payload for <condition>
    When  I send DP863 request to IIB endpoint
    And   I send DP863 request to Azure endpoint
    Then  I can see all the responses are identical for DP863

    Examples:
      | condition                                   | request                |
      | invalid_request                             | cancel_appointment     |
      | booking_cannot_be_cancelled                 | cancel_appointment     |
      | booking_cannot_be_cancelled_for_this_client | cancel_appointment     |


  @negative
  Scenario Outline: Compare DP863 book appointment negative responses between IIB and Azure
    Given I create the DP863 api <request> payload for <condition>
    When  I send DP863 request to IIB endpoint
    And   I send DP863 request to Azure endpoint
    Then  I can see all the responses are identical for DP863

    Examples:
      | condition                                   | request         |
      | timeslot_not_available_preferred_office     | new_appointment |
      | timeslot_not_available_with_staff_member    | new_appointment |


  @negative
  Scenario Outline: Compare DP863 reschedule appointment negative responses between IIB and Azure
    Given I create the DP863 api <request> payload for <condition>
    When  I send DP863 request to IIB endpoint
    And   I send DP863 request to Azure endpoint
    Then  I can see all the responses are identical for DP863

    Examples:
      | condition                                   | request         |
      | timeslot_not_available_preferred_office     | reschedule_appointment |
      | timeslot_not_available_with_staff_member    | reschedule_appointment |


  @negative
  Scenario Outline: Compare DP863 http exception responses
    Given I create the DP863 api <request> payload for <condition>
    When  I send DP863 request to IIB endpoint
    And   I send DP863 request to Azure endpoint
    Then  I can see all the responses are identical for DP863

    Examples:
      | condition                        | request         |
      | error_500_server_exception       | new_appointment |
      | error_500_server_exception       | reschedule_appointment |
      | error_500_server_exception       | cancel_appointment |
