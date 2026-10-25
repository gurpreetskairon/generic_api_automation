@SOAP-API
Feature: Comparison Testing - SC702 - Notify Correspondence Load

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC702 responses are identical

  The user can get the following status:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare SC702 successful transaction response
    Given I create the correct SC702 api payload with different <conditions>
    And   I send the SC702 request to IIB endpoint
    And   I send the SC702 request to Azure endpoint
    Then  I can see all the responses are identical for SC702

    Examples:
      | conditions          |
      | successful_response |
