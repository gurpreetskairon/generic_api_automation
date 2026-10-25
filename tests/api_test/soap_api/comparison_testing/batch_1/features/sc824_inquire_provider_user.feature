@SOAP-API
Feature: Comparison Testing - SC824 - Inquire provider user

  As a client
  I want to compare the responses from the IIB and Azure
  So that I can see whether the responses are identical

  (1) The responses from the IIB and Azure endpoints are identical
  (2) The user can get the following status:
      * 82400 - Transaction Successful
      * 82401 - Participant (i.e. client or provider user) is not recognised.
      * 82402 - Participant detail not available
      * 80099 - Result not recognized

Notes:
* This SC uses a providers, provider members external user account username found in cms
  -CMS Provider home page > Relationships > Provider Members > click name > administration


  @positive
  Scenario: Compare SC824 successful response
    Given I create the correct api payload
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical


  @positive
  Scenario Outline: Compare SC824 client not recognised response
    Given I create the api payload with different <conditions>
    And   I send the inquire provider request to IIB endpoint
    And   I send the inquire provider request to Azure endpoint
    Then  I can see the responses are identical

    Examples:
      | conditions     |
      | not_recognised |
