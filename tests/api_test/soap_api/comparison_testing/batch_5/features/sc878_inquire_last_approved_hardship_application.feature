@AZURE-SOAP-API @SOAP-API @sc878-comparison
Feature: Comparison Testing - SC878 - Inquire Last Approved Hardship Application

  As a client
  I want to send SC878 Inquire Last Approved Hardship Application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 87800 - Transaction Successful
      * 87801 - No matching record
      * 87809 - User not recognised
      * 87810 - Invalid Request
      * 87811 - Client not recognised
    * The expected sub result codes are:
      * 8781001 - Missing client number
      * 8781002 - Invalid client number - Not covered in script(invalid client number triggers schema validation error)
      * 8781101 - Client is a duplicate
      * 8780101 - You do not have access to this client's details


  @positive @sc878-positive
  Scenario Outline: Compare SC878 successful responses between IIB and Azure
    Given I create the SC878 api payload for <condition>
    When  I send SC878 request to IIB endpoint
    And   I send SC878 request to Azure endpoint
    Then  I can see all the responses are identical for SC878

    Examples:
      | condition                              |
      | approved_hardship_application_found    |
      | no_approved_hardship_application_found |


  @negative @sc878-negative
  Scenario Outline: Compare SC878 unsuccessful responses between IIB and Azure
    Given I create the SC878 api payload for <condition>
    When  I send SC878 request to IIB endpoint
    And   I send SC878 request to Azure endpoint
    Then  I can see all the responses are identical for SC878

    Examples:
      | condition                     |
      | user_not_recognised           |
      | missing_client_number         |
      | client_not_recognised         |
      | client_is_duplicate           |
      | client_details_not_accessible |
