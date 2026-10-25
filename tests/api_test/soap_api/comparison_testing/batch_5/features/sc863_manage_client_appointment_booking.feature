@comparison
Feature: Comparison Testing - SC863 - manage client appointment booking

  As a client
  I want to send SC863 manage client appointment bookings to the IIB and Azure endpoints
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
  * when booking an appointment a random case manager is selected in order to reduce the amount of
    failures due to a timeslot being booked already
  * The following fields are excluded during the comparison verification due to the values always
    being different
  ["addDateTime", "id", "identifier", "familyName", "firstName", "fullName", "endDate", "startDate"]
  * Constant failures with the script can cause very few timeslots to be available, changing the
    locationRefId in hte payload body is normally the easiest way to get around these failures



  @positive
  Scenario Outline: Compare SC863 successful responses between IIB and Azure
    Given I create the SC863 api <request> payload for <condition>
    When  I send SC863 request to IIB endpoint
    And   I send SC863 request to Azure endpoint
    Then  I can see all the responses are identical for SC863

    Examples:
      | condition           | request                |
      | successful_response | new_appointment        |
      | successful_response | reschedule_appointment |
      | successful_response | cancel_appointment     |


  @negative
  Scenario Outline: Compare SC863 delete appointment negative responses between IIB and Azure
    Given I create the SC863 api <request> payload for <condition>
    When  I send SC863 request to IIB endpoint
    And   I send SC863 request to Azure endpoint
    Then  I can see all the responses are identical for SC863

    Examples:
      | condition                                   | request                |
      | booking_cannot_be_cancelled                 | cancel_appointment     |
      | booking_cannot_be_cancelled_for_this_client | cancel_appointment     |


  @negative
  Scenario Outline: Compare SC863 book appointment negative responses between IIB and Azure
    Given I create the SC863 api <request> payload for <condition>
    When  I send SC863 request to IIB endpoint
    And   I send SC863 request to Azure endpoint
    Then  I can see all the responses are identical for SC863

    Examples:
      | condition                                   | request         |
      | timeslot_not_available_preferred_office     | new_appointment |
      | timeslot_not_available_with_staff_member    | new_appointment |


  @negative
  Scenario Outline: Compare SC863 reschedule appointment negative responses between IIB and Azure
    Given I create the SC863 api <request> payload for <condition>
    When  I send SC863 request to IIB endpoint
    And   I send SC863 request to Azure endpoint
    Then  I can see all the responses are identical for SC863

    Examples:
      | condition                                   | request         |
      | timeslot_not_available_preferred_office     | reschedule_appointment |
      | timeslot_not_available_with_staff_member    | reschedule_appointment |


  @negative
  Scenario Outline: Compare SC863 http exception responses
    Given I create the SC863 api <request> payload for <condition>
    When  I send SC863 request to IIB endpoint
    And   I send SC863 request to Azure endpoint
    Then  I can see the error responses are identical for SC863

    Examples:
      | condition                        | request         |
      | error_404_uri_not_recognised     | new_appointment |
      | error_401_client_auth_failed     | new_appointment |
      | error_500_server_exception       | new_appointment |
      | error_404_uri_not_recognised     | reschedule_appointment |
      | error_401_client_auth_failed     | reschedule_appointment |
      | error_500_server_exception       | reschedule_appointment |
      | error_404_uri_not_recognised     | cancel_appointment |
      | error_401_client_auth_failed     | cancel_appointment |
