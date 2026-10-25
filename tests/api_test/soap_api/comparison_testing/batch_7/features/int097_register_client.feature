@AZURE-SOAP-API @SOAP-API @int097-comparison
Feature: Comparison Testing - INT097 - Register Client

  As a client,
  I want to send INT097 Register Client requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are functionally equivalent

  Acceptance:
    * The expected successful response is:
      * 00020 - SUCCESS - Client created
    * The expected unsuccessful response is:
      * 00014 - ERROR
    * A fresh valid unused IRD number must be used each time the positive scenario is executed
    * A unique client name must be generated for each successful request
    * IIB and Azure must use different fresh unused IRD numbers because a successful request creates a new client in CMS
    * The returned SWN values are generated client numbers and should not be compared directly


  @skip @positive
  Scenario Outline: Compare INT097 successful response between IIB and Azure
    Given I create the INT097 api payload for <condition>
    When I send INT097 request to IIB endpoint
    And I send INT097 request to Azure endpoint
    Then I can see all the responses are identical for INT097

    Examples:
      | condition              |
      | successful_transaction |

  @negative
  Scenario Outline: Compare INT097 unsuccessful response between IIB and Azure
    Given I create the INT097 api payload for <condition>
    When I send INT097 request to IIB endpoint
    And I send INT097 request to Azure endpoint
    Then I can see all the responses are identical for INT097

    Examples:
      | condition                            |
      | invalid_ird_number_format            |
      | invalid_partner_client_number        |
      | invalid_residency_status_change_date |
      | invalid_person_gender                |
