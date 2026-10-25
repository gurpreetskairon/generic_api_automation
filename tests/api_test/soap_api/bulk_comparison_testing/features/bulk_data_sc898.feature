Feature: Comparison Testing - bulk client data (SC898)

  As I have thousands of client data
  I want to send the requests to each Service Contract in batch 1 to IIB and Azure endpoint
  So that I verify the responses from different endpoints are identical

  Acceptance:
  * All the responses from different Service Contract in batch 1 are identical

  # SC898 IIB may return an empty correlationId element while Azure omits it.
# This technical header element is removed before XML comparison so the bulk test
# validates the actual response content consistently across both endpoints.


  Scenario: Verify bulk client data for SC898
    Given I have updated payloads with the bulk data for SC898
    When  I send the SC898 request to both Azure and IIB endpoints
    Then  I can see all the responses are identical for SC898
