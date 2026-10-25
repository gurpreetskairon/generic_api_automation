@AZURE-SOAP-API @SOAP-API @sc881-comparison
Feature: Comparison Testing - SC881 - Advise Hardship Process Result

  As a client
  I want to send SC881 hardship process result requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 88100 - Transaction Successful
      * 88101 - Transaction Unsuccessful

    * Positive comparison covers both:
      * Non-recoverable Special Needs Grant
      * Recoverable Advance


  @positive @sc881-positive
  Scenario Outline: Compare SC881 successful responses between IIB and Azure
    Given I create the SC881 api payload for <condition>
    When  I send SC881 request to IIB endpoint
    And   I send SC881 request to Azure endpoint
    Then  I can see all the responses are identical for SC881

    Examples:
      | condition                           |
      | non_recoverable_special_needs_grant |
      | recoverable_advance                 |



  @negative @sc881-negative
  Scenario Outline: Compare SC881 unsuccessful responses between IIB and Azure
    Given I create the SC881 api payload for <condition>
    When  I send SC881 request to IIB endpoint
    And   I send SC881 request to Azure endpoint
    Then  I can see all the responses are identical for SC881

    Examples:
      | condition                |
      | Transaction Unsuccessful |

