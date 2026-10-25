@REST-API
Feature: Integration - Get client profile

  As a client
  I want to test the API functionality for getting client profile
  So that I can see see the responses from the server

  The user can get the following status:
  * 200 - Transaction Successful
  * 200 - Has Client Information (Get client flt)
  * 401 - TokenNotPresent
  * 401 - SubscriptionKeyNotFound
  * 400 - Validation error

  Scenario Outline: Check the status of getting client profile
    Given I send a request with different <header>
    Then  I am receiving different status <codes> and service <results>

    Examples:
      | header         | codes | results                 |
      | Get client     | 200   | Transaction Successful  |
      | Get client flt | 200   | Has Client Information  |
      | Token expired  | 401   | TokenNotPresent         |
      | Key missing    | 401   | SubscriptionKeyNotFound |
      | Header missing | 400   | Validation error        |
