@AZURE-SOAP-API @SOAP-API @sc816-comparison
Feature: Comparison Testing - SC816 - Maintain Authorisation

  As a client,
  I want to send SC816 Maintain Authorisation requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 81600 - Transaction successful
      * 81601 - Transaction unsuccessful - no LDAP record linked to this client or provider user

  Execution Note:
    * SC816 supports both client and provider user authorisation.
    * A provider user linked to an External LDAP record has been identified and returns 81600 from IIB.
    * A suitable client linked to an External LDAP record is still required to reproduce the client 81600 scenario.
    * Azure comparison testing will be completed once Azure development is available.


  @positive @sc816-positive
  Scenario Outline: Compare SC816 successful responses between IIB and Azure
    Given I create the SC816 api payload for <condition>
    When I send SC816 request to IIB endpoint
    And I send SC816 request to Azure endpoint
    Then I can see all the responses are identical for SC816

    Examples:
      | condition                    |
#      | successful_client_response   |
      | successful_provider_response |


  @negative @sc816-negative
  Scenario Outline: Compare SC816 no LDAP record responses between IIB and Azure
    Given I create the SC816 api payload for <condition>
    When I send SC816 request to IIB endpoint
    And I send SC816 request to Azure endpoint
    Then I can see all the responses are identical for SC816

    Examples:
      | condition               |
      | client_no_ldap_record   |
      | provider_no_ldap_record |
