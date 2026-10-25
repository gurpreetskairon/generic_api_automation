@SOAP-API
Feature: Comparison Testing - SC852 - Initiate CMS Correspondence

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC852 responses are identical

  Note: The successful scenario requires a unique transaction ID.
 

  @positive
  Scenario Outline: Compare SC852 successful transaction response
    Given I create the correct SC852 api payload with different <conditions>
    And   I send the SC852 request to IIB endpoint
    And   I send the SC852 request to Azure endpoint
    Then  I can see all the responses are identical for SC852

    Examples:
      | conditions          |
      | successful_response |


  @negative
  Scenario Outline: Compare SC852 unsuccessful transaction response
    Given I create the correct SC852 api payload with different <conditions>
    And   I send the SC852 request to IIB endpoint
    And   I send the SC852 request to Azure endpoint
    Then  I can see all the responses are identical for SC852

    Examples:
      | conditions           |
      | no_matching_template |
