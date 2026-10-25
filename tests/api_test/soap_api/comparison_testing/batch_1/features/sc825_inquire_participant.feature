@AZURE-SOAP-API @SOAP-API @sc825-comparison
@inquireparticipant
Feature: Comparison Testing - SC825 - Inquire participant

  As a consumer of the SC825 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC825 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC825 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * Detailed field-level validation is covered under Azure integration testing.

  Execution notes:
  * The same payload is sent to both IIB and Azure for each comparison scenario.
  * Dynamic request values such as auditId, transactionId and requestDateTime are generated once and reused for both endpoints.
  * The temporary_access scenario is included in comparison testing because the test data can be confirmed immediately before execution.
  * The temporary_access client must have active temporary access on the execution date.
  * LDAP/security exception scenarios cover missing header, missing security token and invalid credentials.
  * LDAP/security exception scenarios are currently skipped until the environment/security behaviour is stable for comparison execution.


  @positive @successful_response
  Scenario: Compare SC825 successful response
    Given I create the correct api payload
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC825


  @positive @successful_response @secured_client_access
  Scenario Outline: Compare SC825 successful result and subresult response
    Given I create the correct api payload for <client_type>
    When  I send inquire participant request to IIB endpoint
    And   I send inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC825

    Examples:
      | client_type      |
      | not_secured      |
      | global_access    |
      | temporary_access |


  @negative @soap_action @skip
  Scenario Outline: Compare SC825 responses when SOAPAction is missing or invalid
    Given I create the api payload with different <conditions>
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC825

    Examples:
      | conditions         |
      | invalid SOAPAction |
      | missing SOAPAction |


  @negative @business_response
  Scenario Outline: Compare SC825 responses when the client or user cannot be validated
    Given I create the api payload for <condition>
    When  I send inquire participant request to IIB endpoint
    And   I send inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC825

    Examples:
      | condition          |
      | no_matching_client |
      | no_client_access   |
      | user_not_found     |


  @negative @security_exception @skip
  Scenario Outline: Compare SC825 LDAP exception response when security details are missing or invalid
    Given I create the api payload with different <conditions>
    When  I send inquire participant request to IIB endpoint
    And   I send the inquire participant request to Azure endpoint
    Then  I can see all the responses are identical for SC825

    Examples:
      | conditions             |
      | missing header         |
      | invalid credentials    |
      | missing security token |
