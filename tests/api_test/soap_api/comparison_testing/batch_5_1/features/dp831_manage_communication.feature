@comparison
Feature: Comparison Testing - DP831 - Manage Communication

  As a client
  I want to send DP831 manage communication requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare DP831 successful responses between IIB and Azure
    Given I create the DP831 api payload for <condition>
    When  I send DP831 request to IIB endpoint
    And   I send DP831 request to Azure endpoint
    Then  I can see all the responses are identical for DP831

    Examples:
      | condition                |
      | transaction_successful   |


#  @negative
#  Scenario Outline: Compare DP831 negative responses between IIB and Azure
#    Given I create the DP831 api <payload> payload for <condition>
#    When  I send DP831 request to IIB endpoint
#    And   I send DP831 request to Azure endpoint
#    Then  I can see all the responses are identical for DP831
#
#    Examples:
#      | condition                                 | payload                           |
#      | maximum_character_limit_email_body        | email_and_attachment_notification |
#      | document_name_not_specified               | email_and_attachment_notification |
#      | file_extension_not_specified              | email_and_attachment_notification |
#      | invalid_text_format                       | email_and_attachment_notification |
