@comparison
Feature: Comparison Testing - SC845 - Inquire Obligation

  As a client
  I want to send SC845 soap requests to the IIB and Azure endpoints
  So that I can verify the responses from both endpoints are identical

  Acceptance:
    * The responses from the IIB and Azure endpoints are identical
    * The expected result code are 84500 and 84501
    * Cannot get some of the negative result codes 84502 and 80099 because a 500 status code is returned
      immediately before those result codes can be returned


  @positive @negative
  Scenario Outline: Compare SC845 successful responses between IIB and Azure
    Given I create the SC845 api payload for <condition>
    When  I send SC845 request to IIB endpoint
    And   I send SC845 request to Azure endpoint
    Then  I can see all the responses are identical for SC845

    Examples:
      | condition                |
      | full_time_youth_activity |
      | full_time_work           |
      | no_matching_record       |
