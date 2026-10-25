@AZURE-SOAP-API @SOAP-API @sc730-comparison

Feature: Comparison Testing - SC730 - Notify Document Store

  As a client,
  I want to send SC730 Notify Document Store requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 71000 - Transaction successful
      * 71010 - A document is already registered with this document reference id
      * 71020 - Missing mandatory element
      * 71030 - Request element contains invalid content
      * 71040 - The createdBy userId is unknown

  Execution Note:
    * SC730 is state-changing and a successful scannedImageRef cannot be reused.
    * Successful comparison generates separate unique scannedImageRef values for IIB and Azure.
    * 71030 - Request element contains invalid content is excluded - Relevant data is not available



  @positive
  @sc730-positive
  Scenario Outline: Compare SC730 successful responses between IIB and Azure
    Given I create the SC730 api payload for <condition>
    When I send SC730 request to IIB endpoint
    And I send SC730 request to Azure endpoint
    Then I can see all the responses are identical for SC730

    Examples:
      | condition           |
      | successful_response |


  @negative
  @sc730-negative
  Scenario Outline: Compare SC730 document validation responses between IIB and Azure
    Given I create the SC730 api payload for <condition>
    When I send SC730 request to IIB endpoint
    And I send SC730 request to Azure endpoint
    Then I can see all the responses are identical for SC730

    Examples:
      | condition                    |
      | duplicate_document_reference |


  @negative
  @sc730-negative
  Scenario Outline: Compare SC730 request validation responses between IIB and Azure
    Given I create the SC730 api payload for <condition>
    When I send SC730 request to IIB endpoint
    And I send SC730 request to Azure endpoint
    Then I can see all the responses are identical for SC730

    Examples:
      | condition              |
      | missing_mandatory_data |
#      | invalid_request_data   |


  @negative
  @sc730-negative
  Scenario Outline: Compare SC730 user validation responses between IIB and Azure
    Given I create the SC730 api payload for <condition>
    When I send SC730 request to IIB endpoint
    And I send SC730 request to Azure endpoint
    Then I can see all the responses are identical for SC730

    Examples:
      | condition        |
      | unknown_user     |

