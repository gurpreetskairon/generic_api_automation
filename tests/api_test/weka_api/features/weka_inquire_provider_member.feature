@WEKA_API
Feature: WEKA Inquire Provider Member API

  As an API client
  I want to inquire about provider members through WEKA
  So that I can retrieve member information from the WEKA system

  The user can get the following status:
  * 200 - valid response
  * 409 - invalid response
  * the response body matches the expected_file

  @critical_scenario
  Scenario Outline: Check inquire provider member with valid responses
    Given I would like to send a request with different <external_id>, <external_id_type>, <transaction_id>, <channel_id> and <flt_id>
    Then  I should receive a response with status code 200
    And   I can see the response should match the expected values defined in <expected_file>

    Examples:
      | external_id | external_id_type | transaction_id                       | channel_id | flt_id             | expected_file                   |
      | 292614      | WEKA             | e472c6a6-6c95-4839-be9d-fb888ef6acbg | CIAM       | 12345              | inquire_provider_member         |
      | 292614      | Test             | e472c6a6-6c95-4839-be9d-fb888ef6acbg | CIAM       | Sample_FLT20250807 | inquire_provider_member_invalid |
      | None        | None             | e472c6a6-6c95-4839-be9d-fb888ef6acbg | CIAM       | Sample_FLT20250807 | inquire_provider_member         |


  @critical_scenario
  Scenario Outline: Check inquire provider member with invalid responses
    Given I would like to send a request with different <external_id>, <external_id_type>, <transaction_id>, <channel_id> and <flt_id>
    Then  I should receive a response with status code 409
    Then  I can see the response should match the expected values defined in <expected_file>

    Examples:
      | external_id | external_id_type | transaction_id                       | channel_id | flt_id | expected_file                              |
      | None        | None             | e472c6a6-6c95-4839-be9d-fb888ef6acbg | CIAM       | None   | inquire_provider_member_invalid_flt_id     |
      | None        | None             | None                                 | None       | None   | inquire_provider_member_invalid_channel_id |
