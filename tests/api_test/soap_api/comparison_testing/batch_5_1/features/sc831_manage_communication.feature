@comparison
Feature: Comparison Testing - SC831 - Manage Communication

  As a client
  I want to send SC831 manage communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC831 successful responses between IIB and Azure
    Given I create the SC831 api <payload> payload for <condition>
    When  I send SC831 request to IIB endpoint
    And   I send SC831 request to Azure endpoint
    Then  I can see all the responses are identical for SC831 <condition>

    Examples:
      | condition                | payload                           |
      | transaction_successful   | reapp_notification                |
      | transaction_successful   | email_and_attachment_notification |



  @negative
  Scenario Outline: Compare SC831 negative responses between IIB and Azure
    Given I create the SC831 api <payload> payload for <condition>
    When  I send SC831 request to IIB endpoint
    And   I send SC831 request to Azure endpoint
    Then  I can see all the responses are identical for SC831 <condition>

    Examples:
      | condition                | payload                           |
      | maximum_character_limit_email_body        | email_and_attachment_notification |
      | document_name_not_specified               | email_and_attachment_notification |
      | file_extension_not_specified              | email_and_attachment_notification |
      | invalid_text_format                       | email_and_attachment_notification |
