import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MBIEGetEntitiesDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock route for MBIE NZBN Entity API."""
        # Validate required headers
        required_headers = ["msd-transaction-id"]
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

        # Validate NZBN format (13 digits)
        if not arg.isdigit() or len(arg) != 13:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E003",
                    "httpMessage": "Bad request",
                    "moreInformation": "NZBN must be exactly 13 digits",
                }
            ), 400

        # Simulate not found scenario
        if arg == "9999999999999":
            return jsonify(
                {
                    "httpCode": "404",
                    "messageCode": "MSD-API-E031",
                    "httpMessage": "Resource not found",
                    "moreInformation": "Entity with specified NZBN not found",
                }
            ), 404

        # Success response
        response_data = {
            "nzbn": arg,
            "entityName": "Test Company Limited",
            "entityStatusCode": "REG",
            "entityStatusDescription": "Registered",
            "entityTypeCode": "LTD",
            "entityTypeDescription": "Limited Company",
            "registrationDate": "2020-01-15T09:30:00Z",
            "sourceRegister": "COMPANIES",
            "sourceRegisterUniqueIdentifier": "12345678",
            "lastUpdatedDate": "2024-01-01T12:00:00Z",
            "addresses": {
                "addressList": [
                    {
                        "uniqueIdentifier": "addr-001",
                        "address1": "123 Business Street",
                        "address2": "Level 1",
                        "city": "Wellington",
                        "postCode": "6011",
                        "countryCode": "NZ",
                        "addressType": "REGISTERED",
                    }
                ]
            },
            "phoneNumbers": [
                {
                    "uniqueIdentifier": "phone-001",
                    "phoneCountryCode": "64",
                    "phoneAreaCode": "04",
                    "phoneNumber": "1234567",
                    "phonePurpose": "BUSINESS",
                }
            ],
            "emailAddresses": [
                {
                    "uniqueIdentifier": "email-001",
                    "emailAddress": "contact@testcompany.co.nz",
                    "emailPurpose": "BUSINESS",
                }
            ],
        }

        response_headers = {
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "api-business-govt-nz-Request-Id": request.headers.get("api-business-govt-nz-Request-Id"),
            "api-business-govt-nz-Correlation-Id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
