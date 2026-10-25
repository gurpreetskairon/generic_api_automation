@comparison
Feature: Comparison Testing - SC866 - Process Med Cert

  As a client
  I want to send SC866 process med cert requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC866 successful responses between IIB and Azure
    Given I create the SC866 api payload for <condition>
    When  I send SC866 request to IIB endpoint
    And   I send SC866 request to Azure endpoint
    Then  I can see all the responses are identical for SC866

    Examples:
      | condition           |
      | successful_response |
