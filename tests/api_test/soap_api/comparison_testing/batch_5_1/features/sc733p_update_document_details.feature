@AZURE-SOAP-API @SOAP-API @sc733p-comparison

Feature: Comparison Testing - SC733P - Update Document Details

  As a client,
  I want to send SC733P Update Document Details requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 71000 - Transaction successful
      * 71020 - Missing mandatory element: <value missing>
      * 71070 - Document identifier not recognised
      * 79999 - Unexpected system error - general exception returned with error printstack

  Execution Note:
    * Result code 79999 represents an integration infrastructure/system error and is documented in Acceptance but is not included as a runnable comparison scenario.


  @positive
  @sc733p-positive
  Scenario Outline: Compare SC733P successful responses between IIB and Azure
    Given I create the SC733P api payload for <condition>
    When I send SC733P request to IIB endpoint
    And I send SC733P request to Azure endpoint
    Then I can see all the responses are identical for SC733P

    Examples:
      | condition                                  |
      | successful_response |

  @negative
  @sc733p-negative
  Scenario Outline: Compare SC733P unsuccessful responses between IIB and Azure
    Given I create the SC733P api payload for <condition>
    When I send SC733P request to IIB endpoint
    And I send SC733P request to Azure endpoint
    Then I can see all the responses are identical for SC733P

    Examples:
      | condition                          |
      | missing_mandatory_data             |
      | document_identifier_not_recognised |
