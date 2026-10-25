@AZURE-SOAP-API @SOAP-API @sc869-comparison
Feature: Comparison Testing - SC869 - Create Hardship Application

  As a client
  I want to send SC869 Create Hardship Application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result codes are:
      * 86900 - Transaction Successful
      * 86909 - User not recognised
      * 86910 - Invalid Request
      * 86911 - Client not recognised
      * 86912 - Client record is locked for duplicate or fraud
    * A successfully created application is expected to have status:
      * AA1 - In Progress
    * The hardship need types covered are:
      * N1 - Food
      * N31 - Dental Treatment
      * N68 - School Uniforms
      * N67 - School Stationary

  Execution Note:
    * The request must contain only one application for one client
    * Recipient type SUPPLIER is the valid recipient type for the current implementation
    * Duplicate and fraud client conditions are tested separately but both are expected to return 86912


  @positive @sc869-positive
  Scenario Outline: Compare SC869 successful responses between IIB and Azure
    Given I create the SC869 api payload for <condition>
    When  I send SC869 request to IIB endpoint
    And   I send SC869 request to Azure endpoint
    Then  I can see all the responses are identical for SC869

    Examples:
      | condition                    |
      | successful_food              |
      | successful_dental_treatment  |
      | successful_school_uniform    |
      | successful_school_stationary |


  @negative @sc869-negative
  Scenario Outline: Compare SC869 unsuccessful responses between IIB and Azure
    Given I create the SC869 api payload for <condition>
    When  I send SC869 request to IIB endpoint
    And   I send SC869 request to Azure endpoint
    Then  I can see all the responses are identical for SC869

    Examples:
      | condition             |
      | user_not_recognised   |
      | invalid_request       |
      | client_not_recognised |
