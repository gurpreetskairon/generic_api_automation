@SC575 @AZURE-SOAP-API @integration @inquireparticipant
Feature: Azure Integration - SC575 - Match client details using IRD identifier

  As a consuming system
  I want to submit client identity details to SC575 through the Azure endpoint
  So that I can verify the Azure service returns the expected result code and message

  Acceptance:
    #todo: Sachin


  Background:
    Given I have access to the SC575 Azure endpoint
    And   I have a valid SC575 SOAP request payload


  @PositiveAC01 @positive @match
  Scenario: Verify successful match response when all supplied client details are correct
    Given I create an SC575 payload with valid IRD, name, date of birth and address
    When  I send the request to the Azure endpoint
    Then  the HTTP status code should be 200
    And   the SOAP response result code should be "57500"
    And   the SOAP response message should be "Transaction Successful."
    And   the match outcome should be "Match"


  @PositiveAC02 @positive @no-match
  Scenario Outline: Verify no match response when supplied client details do not match
    Given I create an SC575 payload with a valid IRD
    And   I update the payload with a non-matching "<field>"
    When  I send the request to the Azure endpoint
    Then  the HTTP status code should be 200
    And   the SOAP response result code should be "57500"
    And   the SOAP response message should be "Transaction Successful."
    And   the match outcome should be "No match"

    Examples:
      | field       |
      | name        |
      | dateOfBirth |


  @NegativeAC01 @negative @request-validation @transaction-id
  Scenario Outline: Verify validation response when transactionId is missing or invalid
    Given I create an SC575 payload with "<transaction_id_condition>"
    When  I send the request to the Azure endpoint
    Then  the HTTP status code should be 200
    And   the SOAP response result code should be "57503"
    And   the SOAP response message should be "Transaction Id is missing or format invalid."

    Examples:
      | transaction_id_condition     |
      | invalid transactionId format |
      | blank transactionId          |


  @NegativeAC02 @negative @request-validation
  Scenario Outline: Verify validation response when mandatory request parameters are missing or invalid
    Given I create an SC575 payload with invalid or missing "<field>" using "<condition>"
    When  I send the request to the Azure endpoint
    Then  the HTTP status code should be 200
    And   the SOAP response result code should be "57501"
    And   the SOAP response message should be "The request parameters are invalid."

    Examples:
      | field   | condition                 |
      | IRD     | number less than 9 digits |
      | IRD     | number more than 9 digits |
      | IRD     | blank value               |
      | IRD     | identifier block removed  |
      | name    | blank value               |
      | name    | name block removed        |
      | address | blank value               |


  @NegativeAC03 @negative @ird @business-validation
  Scenario: Verify validation response when IRD is 9 digits but not valid for the customer type
    Given I create an SC575 payload with a 9 digit IRD number that is not valid or does not match the customer type
    When  I send the request to the Azure endpoint
    Then  the HTTP status code should be 200
    And   the SOAP response result code should be "57502"
    And   the SOAP response message should be "Unstructured IRD number supplied or not match the customer type."
