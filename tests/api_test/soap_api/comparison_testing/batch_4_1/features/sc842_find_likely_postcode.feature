
@AZURE-SOAP-API @SOAP-API @sc842-comparison
Feature: Comparison Testing - SC842 - Find Likely Postcode
  As a client,
  I want to send SC842 Find Likely Postcode requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 84200 - Transaction Successful (one or more postcodes match the query)
      * 84201 - No matching record (no postcodes match the query)
      * 84202 - Invalid request (an invalid request is submitted)
    * AddressId is not validated by this service

  @positive @sc842-positive
  Scenario Outline: Compare SC842 successful responses between IIB and Azure
    Given I create the SC842 api payload for <condition>
    When I send SC842 request to IIB endpoint
    And I send SC842 request to Azure endpoint
    Then I can see all the responses are identical for SC842

    Examples:
      | condition          |
      | matching_postcode  |
      | no_matching_record |

#  @negative @sc842-negative
#  Scenario Outline: Compare SC842 unsuccessful responses between IIB and Azure
#    Given I create the SC842 api payload for <condition>
#    When I send SC842 request to IIB endpoint
#    And I send SC842 request to Azure endpoint
#    Then I can see all the responses are identical for SC842
#
#    Examples:
#      | condition       |
#      | invalid_request |
