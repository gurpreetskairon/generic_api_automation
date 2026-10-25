@AZURE-SOAP-API @SOAP-API @sc807-comparison
@managedebt @createdebtandredirections
Feature: Comparison Testing - SC807 - Create debt and redirections

  As a consumer of the SC807 SOAP service
  I want to compare the responses from IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC807 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC807 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * A successful request that creates debt and redirections returns result code 80700 and message Debt and redirections received successfully by service provider.
  * A successful request that creates debt without redirections returns result code 80701 and message Transaction successful.
  * A request where debt and redirections cannot be created returns result code 80702 and message Transaction unsuccessful.
  * An invalid request returns result code 80710 and message Invalid request.
  * A request containing a client number that does not exist returns result code 80711 and message Client not recognised.

  Execution notes:
  * The same payload is sent to both IIB and Azure for each comparison scenario.
  * Only one client number is populated in each request.
  * Only one product ID is populated in each request.
  * Only one debt is populated in each request.
  * The request may contain debt only, debt with redirections, or redirections only.
  * The breach type and other master-data values must be recognised by the service provider.
  * A payment record must be available when an existing EHC contribution redirection is deleted.
  * The redirection payment amount must be valid.
  * The redirection pay-period end date must be after the pay-period start date.


  @positive
  Scenario Outline: Compare SC807 successful create debt and redirections responses
    Given I create the SC807 api payload for <condition>
    When  I send SC807 create debt and redirections request to IIB endpoint
    And   I send SC807 create debt and redirections request to Azure endpoint
    Then  I can see all the responses are identical for SC807

    Examples:
      | condition                        |
      | successful_debt_and_redirections |
      | successful_debt_only             |


  @negative
  Scenario Outline: Compare SC807 unsuccessful and invalid request responses
    Given I create the SC807 api payload for <condition>
    When  I send SC807 create debt and redirections request to IIB endpoint
    And   I send SC807 create debt and redirections request to Azure endpoint
    Then  I can see all the responses are identical for SC807

    Examples:
      | condition                |
      | transaction_unsuccessful |
      | invalid_request          |
      | client_not_recognised    |
