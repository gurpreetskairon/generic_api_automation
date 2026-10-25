@SOAP-API
@DP762-comparison
Feature: Comparison Testing - DP762 - Find Service Locations

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  Acceptance:
  * Get matching responses from the IIB and Azure endpoints


  @positive
  Scenario Outline: Compare DP762 successful response
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions                           |
      | service_locations_found              |
      | service_locations_found_by_city_only |


  @negative
  Scenario Outline: Compare DP762 responses for no service locations found
    Given I create the correct api payload with different <conditions>
    And   I send the request to IIB endpoint
    And   I send the request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions                 |
      | no_service_locations_found |
