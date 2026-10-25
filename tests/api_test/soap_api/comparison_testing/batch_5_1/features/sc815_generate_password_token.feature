@AZURE-SOAP-API @SOAP-API @sc815-comparison
Feature: Comparison Testing - SC815 - Generate Password Token

  As a client,
  I want to send SC815 Generate Password Token requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 81500 - Transaction successful
      * 81501 - Verification failed as My Account status is inactive
      * 81502 - Verification failed as My Account status is locked
      * 81503 - Verification failed - check death date
      * 81504 - Verification failed - technical fault
      * 80099 - Result not recognized

  Execution Note:
    * Result codes 81501, 81502 and 81503 apply when client verification is required.
    * Result code 81504 represents unexpected or technical failures and requires a reproducible backend condition before it can be automated.
    * Result code 80099 depends on the providing system returning an unrecognised result and requires a reproducible condition before it can be automated.

  @positive @sc815-positive
  Scenario Outline: Compare SC815 successful responses between IIB and Azure
    Given I create the SC815 api payload for <condition>
    When I send SC815 request to IIB endpoint
    And I send SC815 request to Azure endpoint
    Then I can see all the responses are identical for SC815

    Examples:
      | condition                    |
      | successful_client_response   |
      | successful_provider_response |

#  @negative @sc815-negative
#  Scenario Outline: Compare SC815 verification failure responses between IIB and Azure
#    Given I create the SC815 api payload for <condition>
#    When I send SC815 request to IIB endpoint
#    And I send SC815 request to Azure endpoint
#    Then I can see all the responses are identical for SC815
#
#    Examples:
#      | condition                       |
#      | client_authorisation_inactive   |
#      | client_authorisation_locked     |
#      | client_deceased                 |
