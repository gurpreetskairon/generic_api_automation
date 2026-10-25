@comparison
Feature: Comparison Testing - SC586 - Publish Cmsparticipant

  As a client
  I want to send SC586 publish cmsparticipant requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical

  Notes:
    * There are 2 payloads for this testing, 1 creates/edits a child, another creates/edit a client
    * The request sent CAN be asynchronous or synchronous
      from the documentation: (In the event that the service call is processed synchronously, then
      instead of an acknowledgement response, a synchronous response is returned immediately.
      In this case, the service will return the exact same post conditions and result codes as given
      for Callback Response in 1.4.2 above. Note that under certain conditions, the service may
      decide to process the request synchronously, even where the request has designated the
      interaction as asynchronous (request/acknowledgement/callback interaction pattern).


  @positive
  Scenario Outline: Compare SC586 successful responses between IIB and Azure for adding and editing a child record
    Given I create the SC586 api <payload> payload for <condition>
    When  I send SC586 request to IIB endpoint
    And   I send SC586 request to Azure endpoint
    Then  I can see all the responses are identical for SC586

    Examples:
      | condition                    | payload    |
      | processing_successful_swiftt | add_child  |
      | processing_queued_wam        | add_child  |
      | 19_year_old_child_swiftt     | add_child  |
      | processing_successful_swiftt | edit_child |
      | processing_queued_wam        | edit_child |
      | 19_year_old_child_swiftt     | edit_child |


  @positive
  Scenario Outline: Compare SC586 successful responses between IIB and Azure for adding and editing a client record
    Given I create the SC586 api <payload> payload for <condition>
    When  I send SC586 request to IIB endpoint
    And   I send SC586 request to Azure endpoint
    Then  I can see all the responses are identical for SC586

    Examples:
      | condition                    | payload     |
      | processing_successful_swiftt | add_client  |
      | processing_queued_wam        | add_client  |
      | processing_successful_swiftt | edit_client |
      | processing_queued_wam        | edit_client |


  @positive
  Scenario Outline: Compare SC586 successful responses between IIB and Azure for negative scenarios
    Given I create the SC586 api <payload> payload for <condition>
    When  I send SC586 request to IIB endpoint
    And   I send SC586 request to Azure endpoint
    Then  I can see all the responses are identical for SC586

    Examples:
      | condition               | payload    |
      | unexpected_error_swiftt | add_child  |
      | unexpected_error_swiftt | edit_child |
      | unexpected_error_swiftt | add_client |
