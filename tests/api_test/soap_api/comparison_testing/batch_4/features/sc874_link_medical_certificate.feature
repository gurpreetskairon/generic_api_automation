@IIB-AZURE-COMPARISON @SOAP-API @sc874-comparison @COMPARISON-SOAP-API
Feature: Comparison Testing - SC874 - Link Medical Certificate

  # SC874 Test Data Notes
  #
  # 87400 - Transaction Successful
  #         Valid client and medical certificate already linked to the same client.
  #
  # 87409 - User Not Recognised
  #         Invalid security token user.
  #
  # 87413 - Medical Certificate Not Recognised
  #         Medical certificate identifier does not exist.
  #
  # 87414 - Medical Certificate Linked to Different Client
  #         Medical certificate is already linked to another client.


  @positive
  Scenario Outline: Compare SC874 successful transaction response
    Given I create the correct SC874 api payload with different <conditions>
    And   I send the SC874 request to IIB endpoint
    And   I send the SC874 request to Azure endpoint
    Then  I can see all the responses are identical for SC874

    Examples:
      | conditions             |
      | successful_transaction |


  @negative
  Scenario Outline: Compare SC874 unsuccessful transaction response
    Given I create the correct SC874 api payload with different <conditions>
    And   I send the SC874 request to IIB endpoint
    And   I send the SC874 request to Azure endpoint
    Then  I can see all the responses are identical for SC874

    Examples:
      | conditions                             |
      | user_not_recognised                    |
      | medical_certificate_not_recognised     |
      | certificate_linked_to_different_client |
      | client_locked_duplicate_fraud          |
