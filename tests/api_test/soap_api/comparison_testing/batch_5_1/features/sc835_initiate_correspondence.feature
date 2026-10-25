@SOAP-API
Feature: Comparison Testing - SC835 - Initiate Correspondence

  As a client
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC835 responses are consistent

  The service can return the following tested outcomes:
  * 83500 - Transaction Successful
  * 83501 - No Matching Template


  @positive
Scenario Outline: Compare SC835 successful transaction response
  Given I create the correct SC835 api payload with different <conditions>
  And I send the SC835 request to IIB endpoint
  And I send the SC835 request to Azure endpoint
  Then I can see all the responses are identical for SC835

  Examples:
    | conditions          |
    | successful_response |


  @negative
Scenario Outline: Compare SC835 no matching template response
  Given I create the correct SC835 api payload with different <conditions>
  And I send the SC835 request to IIB endpoint
  And I send the SC835 request to Azure endpoint
  Then I can see all the responses are identical for SC835

  Examples:
    | conditions           |
    | no_matching_template |
