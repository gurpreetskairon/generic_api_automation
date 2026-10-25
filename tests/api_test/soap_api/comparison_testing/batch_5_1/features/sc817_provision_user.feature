@AZURE-SOAP-API @SOAP-API @sc817-comparison
Feature: Comparison Testing - SC817 - Provision User

  As a client,
  I want to send SC817 Provision User requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 81700 - Transaction successful
      * 81701 - The client number/provider user number and one-time password details are incorrect
      * 81702 - The maximum number of attempts permitted to correctly enter client number/provider user number and one-time password has been exceeded
      * 81703 - The one-time password has expired
      * 81704 - User Locked Temporarily

    Execution Note:
    * SC817 depends on an OTP generated through SC815.
    * Successful OTP validation consumes the OTP and cannot be repeated.
    * Currently, only provider test data is available.
    * Maximum attempts exceeded and temporary locked scenarios require specific account states.
    * Client and successful OTP scenarios are excluded from runnable automation due to test-data dependencies.
    * IIB and Azure comparison may be affected by shared backend state.

#  @positive @sc817-positive @sc817-client
#  Scenario Outline: Compare SC817 successful client provisioning responses between IIB and Azure
#    Given I create the SC817 api payload for <condition>
#    When I send SC817 request to IIB endpoint
#    And I send SC817 request to Azure endpoint
#    Then I can see all the responses are identical for SC817
#
#    Examples:
#      | condition                   |
#      | successful_client_response  |
#
#
#  @positive @sc817-positive @sc817-provider
#  Scenario Outline: Compare SC817 successful provider provisioning responses between IIB and Azure
#    Given I create the SC817 api payload for <condition>
#    When I send SC817 request to IIB endpoint
#    And I send SC817 request to Azure endpoint
#    Then I can see all the responses are identical for SC817
#
#    Examples:
#      | condition                     |
#      | successful_provider_response  |


  @negative @sc817-negative
  Scenario Outline: Compare SC817 unsuccessful authentication responses between IIB and Azure
    Given I create the SC817 api payload for <condition>
    When I send SC817 request to IIB endpoint
    And I send SC817 request to Azure endpoint
    Then I can see all the responses are identical for SC817

    Examples:
      | condition                    |
#      | incorrect_business_key_otp   |
      | maximum_attempts_exceeded    |
#      | expired_otp                  |
#      | user_temporarily_locked      |
