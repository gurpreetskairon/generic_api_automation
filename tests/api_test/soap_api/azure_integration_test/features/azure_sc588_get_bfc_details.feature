@REST-API @getbfcdetails
Feature: Comparison Testing - SC588 - Get BFC Details

  As a client
  I want to send SOAP requests to the Azure api and verify the response
  So that I can verify the messages in the response


  Scenario Outline: Verify SC588 unauthorized response
    Given I create the correct SC588 api payload with different <conditions>
    And I send the SC588 request to Azure endpoint
    Then I can see Invalid Credentials displayed in the response

    Examples:
      | conditions              |
      | missing_authorization   |
      | invalid_authorization   |
