@WEKA_API
Feature: WEKA Participant Link Account API

  As an API client
  I want to link FLT details to participant accounts through WEKA
  So that I can associate identities with participants in the WEKA system

  The user can get the following status:
  * 200 - valid response
  * 409 - invalid response
  * the response body matches the expected_file

  @critical_scenario
  Scenario Outline: test participant Idp link API if flt can be updated successfully for given alternateid
    Given I would like to send a request with different <transaction_id> , <channel_id>, <alternate_id> , <flt>, <privacy_domain>, <idp>, <ciam_id> and <reference_type_code>
    Then I should receive a response with status code 200
    And the API response body and status should match the expected <expected_file>

    Examples:
      | transaction_id                       | channel_id | alternate_id | flt      | privacy_domain                        | idp    | reference_type_code | ciam_id                              | expected_file        |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 374313       | AutoTest | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | 1a4bd3c0-3827-11eb-adc1-0242ac120002 | participant_Idp_link |

  @critical_scenario
  Scenario Outline: Verify error when send an invalid or blank data
    Given I would like to send a request with different <transaction_id> , <channel_id>, <alternate_id> , <flt>, <privacy_domain>, <idp>, <ciam_id> and <reference_type_code>
    Then I should receive a response with status code 409
    And the API response body and status should match the expected <expected_file>

    Examples:
      | transaction_id                       | channel_id | alternate_id    | flt                                 | privacy_domain                        | idp    | reference_type_code | ciam_id                              | expected_file                              |
      | None                                 | CIAM       | 300000070156755 | AZU6A5605BCAC244C25811E4584172ECB33 | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_empty_attribute_error |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | None       | 300000070156755 | AZU6A5605BCAC244C25811E4584172ECB33 | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_empty_attribute_error |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | None            | AZU6A5605BCAC244C25811E4584172ECB33 | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_empty_attribute_error |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 300000070156755 | None                                | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_empty_attribute_error |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 300000070156755 | AZU6A5605BCAC244C25811E4584172ECB33 | None                                  | REALME | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_empty_attribute_error |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 300000070156755 | AZU6A5605BCAC244C25811E4584172ECB33 | https://msd.govt.nz/provders/CIAM-Dev | None   | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_empty_attribute_error |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 300000070156755 | AZU6A5605BCAC244C25811E4584172ECB33 | https://msd.govt.nz/provders/CIAM-Dev | REALME | None                | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_empty_attribute_error |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 300000070156755 | AZU6A5605BCAC244C25811E4584172ECB33 | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | None                                 | participant_Idp_link_empty_attribute_error |


  @critical_scenario
  Scenario Outline: invalid API token should throw error
    Given I would like to send a request with different <transaction_id> , <channel_id>, <alternate_id> , <flt>, <privacy_domain>, <idp>, <ciam_id> and <reference_type_code>
    Then I should receive a response with status code 401
    And the API response body and status should match the expected <expected_file>

    Examples:
      | transaction_id                       | channel_id | alternate_id    | flt           | privacy_domain                        | idp    | reference_type_code | ciam_id                              | expected_file                            |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 300000070156755 | INVALID_TOKEN | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_invalid_token_error |

  @critical_scenario
  Scenario Outline: Send request with an alternate id which does not exist in CMS throws error
    Given I would like to send a request with different <transaction_id> , <channel_id>, <alternate_id> , <flt>, <privacy_domain>, <idp>, <ciam_id> and <reference_type_code>
    Then I should receive a response with status code 200
    And the API response body and status should match the expected <expected_file>

    Examples:

      | transaction_id                       | channel_id | alternate_id | flt                                 | privacy_domain                        | idp    | reference_type_code | ciam_id                              | expected_file                                   |
      | b724ebd0-0c71-4a01-a8e1-43f33bfa4feb | CIAM       | 99999        | AZU6A5605BCAC244C25811E4584172ECB33 | https://msd.govt.nz/provders/CIAM-Dev | REALME | CA7                 | 72c55a6c-bda5-488e-b4c9-d3c240576gb1 | participant_Idp_link_invalid_alternate_id_error |
