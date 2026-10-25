Feature: Comparison Testing - DP152 Manage Job Search Activity

  As a client
  I want to send DP152 requests to the IIB and Azure endpoints
  So that I can verify the responses are identical


  DP152 supports both methods:
   1) POST — Create a new Job Search Activity under an existing action_id
   2) PUT — Update an existing activity using its action_id and job_search_activity_id


  Scenario Outline: Compare DP152 successful transaction response
    Given I create the correct DP152 api request with different <conditions>
    And I send the DP152 request to IIB endpoint
    And I send the DP152 request to Azure endpoint
    Then I can see all the responses are identical for DP152

    Examples:
      | conditions             |
      | successful_transaction |

 #POST method
  Scenario Outline: Compare DP152 invalid request response
    Given I create the correct DP152 api request with different <conditions>
    And I send the DP152 request to IIB endpoint
    And I send the DP152 request to Azure endpoint
    Then I can see all the responses are identical for DP152

    Examples:
      | conditions      |
      | invalid_request |

   #PUT method
  Scenario Outline: Compare DP152 successful update response
    Given I create the correct DP152 update api request with different <conditions>
    And I send the DP152 update request to IIB endpoint
    And I send the DP152 update request to Azure endpoint
    Then I can see all the DP152 update responses are identical

    Examples:
      | conditions        |
      | successful_update |


  Scenario Outline: Compare DP152 invalid update response
    Given I create the correct DP152 update api request with different <conditions>
    And I send the DP152 update request to IIB endpoint
    And I send the DP152 update request to Azure endpoint
    Then I can see all the DP152 update responses are identical

    Examples:
      | conditions     |
      | invalid_update |
