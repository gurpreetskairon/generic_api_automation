@REST-API
Feature: Integration - Client drug test


  As a client
  I want to test the API functionality for client drug test
  So that I can see see the responses from the server

  The user can get the following status:
  * 200 - Transaction Successful
  * 401 - TokenNotPresent
  * 401 - SubscriptionKeyNotFound
  * 400 - Validation error

  Scenario Outline: Check the status of client drug test
    Given I send a request with different <header>
    Then  I am receiving different status <codes> and service <results>

    Examples:
      | header                   | codes | results                 |
      | Check drug test referral | 200   | Transaction Successful  |
      | Token missing            | 401   | TokenNotPresent         |
      | Key missing              | 401   | SubscriptionKeyNotFound |
      | Header missing           | 400   | Validation error        |
