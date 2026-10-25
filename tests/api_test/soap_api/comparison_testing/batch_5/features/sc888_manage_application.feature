@comparison
Feature: Comparison Testing - SC888 - Manage Application

  As a client
  I want to send SC888 manage application requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical


  @positive
  Scenario Outline: Compare SC888 successful responses between IIB and Azure for id verification
    Given I create the SC888 api <payload_type> for <condition>
    When  I send SC888 request to IIB endpoint
    And   I send SC888 request to Azure endpoint
    Then  I can see all the responses are identical for SC888

    Examples:
      | condition            | payload_type    |
      | ID_PROVIDED          | id_verification |
      | CANNOT_PROVIDE       | id_verification |
      | NO_DOCS              | id_verification |
      | ACKNOWLEDGE_TO_BRING | id_verification |


  @positive
  Scenario Outline: Compare SC888 successful responses between IIB and Azure for obligation verification
    Given I create the SC888 api <payload_type> for <condition>
    When  I send SC888 request to IIB endpoint
    And   I send SC888 request to Azure endpoint
    Then  I can see all the responses are identical for SC888

    Examples:
      | condition             | payload_type             |
      | OBLIGATIONS_ACCEPTED  | obligations_verification |
      | OBLIGATIONS_DISCUSSED | obligations_verification |


  @negative
  Scenario Outline: Compare SC888 successful responses between IIB and Azure for negative scenarios
    Given I create the SC888 api <payload_type> for <condition>
    When  I send SC888 request to IIB endpoint
    And   I send SC888 request to Azure endpoint
    Then  I can see all the responses are identical for SC888

    Examples:
      | condition             | payload_type             |
#      | INVALID_CASEREFERENCE | obligations_verification |
#      | MISSING_CASEREFERENCE | obligations_verification |
#      | CLIENT_NOT_RECOGNISED | obligations_verification |
#      | INVALID_SWN           | obligations_verification |
      | USER_NOT_RECOGNISED   | obligations_verification |
#      | INVALID_CASEREFERENCE | id_verification          |
#      | MISSING_CASEREFERENCE | id_verification          |
#      | CLIENT_NOT_RECOGNISED | id_verification          |
#      | INVALID_SWN           | id_verification          |
      | USER_NOT_RECOGNISED   | id_verification          |

