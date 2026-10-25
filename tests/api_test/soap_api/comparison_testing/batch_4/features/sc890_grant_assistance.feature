@SOAP-API
Feature: Comparison Testing - SC890 - Grant Assistance

  As a client,
  I want to compare the responses from IIB and Azure
  So that I can confirm the SC890 responses are consistent


  @positive
  Scenario Outline: Compare SC890 successful transaction response
    Given I create the correct SC890 api payload with different <conditions>
    And   I send the SC890 request to IIB endpoint
    And   I send the SC890 request to Azure endpoint
    Then  I can see all the responses are identical for SC890

    Examples:
      | conditions              |
      | grant_assistance_failed |


#  @negative
#Scenario Outline: Compare SC890 unsuccessful transaction response
#  Given I create the correct SC890 api payload with different <conditions>
#  And I send the SC890 request to IIB endpoint
#  And I send the SC890 request to Azure endpoint
#  Then I can see all the responses are identical for SC890
#
#  Examples:
#    | conditions            |
#    | invalid_income_type |
