import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MSDProviderInquireDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        alternate_id = request.args.get("alternateID")
        external_id = request.args.get("externalID")
        external_id_type = request.args.get("externalIDType")
        flt_id = request.args.get("fltID")

        # Validate required headers
        required_headers = [
            "msd-transaction-id",
            "msd-request-date-time",
            "msd-channel-id",
        ]
        missing_headers = [header for header in required_headers if header not in request.headers]

        if missing_headers:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": f"Missing required headers: {', '.join(missing_headers)}",
                }
            ), 400
        # Validate required parameters
        if not (alternate_id or flt_id or external_id):
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": "Please provide at least one parameter from alternateID, externalID or fltID",
                }
            ), 400

        # Validate external ID type if external ID is provided
        if external_id and not external_id_type:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": "Please provide externalid with externalidtype",
                }
            ), 400

        # Validate external ID type value
        if external_id_type and external_id_type != "CIAM":
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E003",
                    "httpMessage": "Bad request",
                    "moreInformation": "Provider error : There was an issue while parsing a 'externalIDType' attribute, which contains a value of 'TEST': The field &#39;externalIDType&#39; has an invalid option selected, &#39;TEST&#39;. Please select a valid option.",
                }
            ), 400

        response_data = {
            "providerMemberDetails": [
                {
                    "referenceNumber": "123456789012345678",
                    "name": "John Doe",
                    "status": {
                        "tableName": "StatusTable",
                        "value": "Active",
                        "description": "Active status",
                    },
                    "startDate": "2021-01-01",
                    "endDate": "2022-01-01",
                    "providerExternalIDList": [
                        {
                            "providerExternalID": "12345678-1234-1234-1234-123456789012",
                            "providerExternalIDType": {
                                "tableName": "ExternalIDTypeTable",
                                "value": "Type1",
                                "description": "Type 1",
                            },
                        }
                    ],
                    "providerMemberExternalIDList": [
                        {
                            "externalID": "12345678-1234-1234-1234-123456789012",
                            "externalIDType": {
                                "tableName": "ExternalIDTypeTable",
                                "value": "Type1",
                                "description": "Type 1",
                            },
                        }
                    ],
                    "fltDetailsList": [
                        {
                            "fltID": "FLT12345",
                            "privacyDomain": "string",
                            "idpEntity": {
                                "tableName": "string",
                                "value": "string",
                                "description": "string",
                                "parentCodeTable": "string",
                            },
                        }
                    ],
                    "providerDetails": [
                        {
                            "nzBizNumber": "123456789",
                            "charityNumber": "1234567",
                            "companyNumber": "1234567",
                            "irdNumber": "123456789",
                            "name": "Provider Name",
                            "knownAs": "Provider Known As",
                            "referenceNumber": "123456789012345678",
                        }
                    ],
                    "positionList": [
                        {
                            "position": {
                                "tableName": "PositionTable",
                                "value": "Position1",
                                "description": "Position 1",
                            }
                        }
                    ],
                    "roleList": [
                        {
                            "role": {
                                "tableName": "RoleTable",
                                "value": "Role1",
                                "description": "Role 1",
                            }
                        }
                    ],
                    "emailAddressList": [
                        {
                            "emailAddress": "john.doe@example.com",
                            "isPrimaryInd": True,
                            "type": {
                                "tableName": "EmailTypeTable",
                                "value": "Work",
                                "description": "Work Email",
                            },
                        }
                    ],
                    "addressList": [
                        {
                            "isPrimaryInd": True,
                            "type": {
                                "tableName": "AddressTypeTable",
                                "value": "Home",
                                "description": "Home Address",
                            },
                            "addressLine1": "123 Main St",
                            "addressLine2": "Apt 4B",
                            "city": "Anytown",
                            "suburb": "Anysuburb",
                            "country": "Anycountry",
                            "postCode": "12345",
                            "addressLine3": "Address Line 3",
                            "careOfAddress": "Care Of Address",
                        }
                    ],
                    "phoneNumberList": [
                        {
                            "isPrimaryInd": True,
                            "type": {
                                "tableName": "PhoneTypeTable",
                                "value": "Mobile",
                                "description": "Mobile Phone",
                            },
                            "countryCode": "1",
                            "areaCode": "123",
                            "phoneNumber": "5551234567",
                            "extension": "123",
                        }
                    ],
                }
            ]
        }

        response_headers = {
            "msd-channel-id": request.headers.get("msd-channel-id"),
            "msd-request-date-time": request.headers.get("msd-request-date-time"),
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "msd-correlation-id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
