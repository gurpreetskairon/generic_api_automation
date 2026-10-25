@AZURE-SOAP-API @SOAP-API @sc532-comparison
@getproductdeliverydetails
Feature: Comparison Testing - SC532V2 - Get product delivery details

  As a consumer of the SC532V2 SOAP service
  I want to compare the responses returned by IIB and Azure
  So that I can confirm Azure behaviour is aligned with IIB for the agreed SC532V2 scenarios

  Acceptance:
  * Azure and IIB responses should be identical for the covered SC532V2 comparison scenarios.
  * XML namespace prefixes are not treated as business-data differences.
  * A successful request where Product Delivery details exist returns result code 50000 and message Transaction successful.
  * An active-only request where no active Product Delivery details exist returns the applicable provider-system response.
  * A request for an existing client with no matching Product Delivery record returns result code 53201 and message No matching record.
  * A request for a client number that does not exist in SWIFTT returns result code 53201 and message Client not recognised.
  * When productTypeCode filters are supplied, only the requested product types should be returned.
  * Detailed business-field validation is handled separately from this comparison feature.

  Execution notes:
  * The same payload is sent to both IIB and Azure for each comparison scenario.
  * Dynamic request values are generated once and reused for both endpoints.
  * Product Delivery details are requested for both Seniors and WorkAndIncome service lines.
  * The successful_response condition explicitly requests all supported product types.
  * The successful_without_product_type_filter condition does not populate productTypeCode.
  * The Supplementary-only 53203 condition is excluded because it is no longer included in the acceptance criteria.


  @positive @product_type_filters
  Scenario Outline: Compare SC532V2 successful and filtered responses
    Given I create the SC532V2 api payload for <condition>
    When  I send SC532V2 get product delivery details request to IIB endpoint
    And   I send SC532V2 get product delivery details request to Azure endpoint
    Then  I can see all the responses are identical for SC532V2

    Examples:
      | condition                              |
      | successful_response                    |
      | successful_without_product_type_filter |
      | successful_primary_filter              |
      | successful_secondary_filter            |


  @positive @no_active_product_delivery
  Scenario: Compare SC532V2 no active product delivery response
    Given I create the SC532V2 api payload for no_active_product_delivery
    When  I send SC532V2 get product delivery details request to IIB endpoint
    And   I send SC532V2 get product delivery details request to Azure endpoint
    Then  I can see all the responses are identical for SC532V2


  @negative
  Scenario Outline: Compare SC532V2 unsuccessful responses
    Given I create the SC532V2 api payload for <condition>
    When  I send SC532V2 get product delivery details request to IIB endpoint
    And   I send SC532V2 get product delivery details request to Azure endpoint
    Then  I can see all the responses are identical for SC532V2

    Examples:
      | condition             |
      | no_matching_record    |
      | client_not_recognised |
