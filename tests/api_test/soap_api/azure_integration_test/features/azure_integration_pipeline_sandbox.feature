@AZURE-SOAP-API @SOAP-API
@sandbox
Feature: integration-pipeline-sandbox azure integration testing


  Scenario: Check sandbox response schema
    Given I created the correct sandbox api payload
    When  I sent the sandbox request to the Azure endpoint
    Then  I can see the sandbox response schema returned
