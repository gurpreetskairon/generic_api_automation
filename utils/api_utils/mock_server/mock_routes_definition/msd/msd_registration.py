import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MSDRegistrationDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Handle prospect person registration requests."""
        # Validate required headers
        required_headers = [
            "msd-transaction-id",
            "msd-request-date-time",
            "msd-channel-id",
        ]

        missing_headers = [header for header in required_headers if header.lower() not in request.headers]
        if missing_headers:
            return (
                jsonify(
                    {
                        "httpCode": "400",
                        "messageCode": "MSD-API-E001",
                        "httpMessage": "Bad request",
                        "moreInformation": f"Missing required headers: {', '.join(missing_headers)}",
                    }
                ),
                400,
                {},
            )

        data = request.json
        if not data:
            return (
                jsonify(
                    {
                        "httpCode": "400",
                        "messageCode": "MSD-API-E001",
                        "httpMessage": "Bad request",
                        "moreInformation": "Request body is required",
                    }
                ),
                400,
                {},
            )  # Validate required fields in request body
        required_fields = ["nameList", "sourceSystem"]
        if data:
            missing_fields = [field for field in required_fields if field not in data]
        else:
            missing_fields = required_fields
        if missing_fields:
            return (
                jsonify(
                    {
                        "httpCode": "400",
                        "messageCode": "MSD-API-E001",
                        "httpMessage": "Bad request",
                        "moreInformation": f"Missing required fields: {', '.join(missing_fields)}",
                    }
                ),
                400,
                {},
            )

        # Validate nameList structure
        if not data.get("nameList") or not isinstance(data["nameList"], list):
            return (
                jsonify(
                    {
                        "httpCode": "400",
                        "messageCode": "MSD-API-E001",
                        "httpMessage": "Bad request",
                        "moreInformation": "nameList must be a non-empty array",
                    }
                ),
                400,
                {},
            )

        # Validate each name in nameList
        for name in data["nameList"]:
            required_name_fields = ["firstName", "lastName", "type"]
            missing_name_fields = [field for field in required_name_fields if field not in name]
            if missing_name_fields:
                return (
                    jsonify(
                        {
                            "httpCode": "400",
                            "messageCode": "MSD-API-E001",
                            "httpMessage": "Bad request",
                            "moreInformation": f"Missing required fields in nameList: {', '.join(missing_name_fields)}",
                        }
                    ),
                    400,
                    {},
                )

        # Success response
        response_data = {"referenceNumber": "123456789012345678"}

        # Return headers as specified in OpenAPI spec
        response_headers = {
            "msd-channel-id": request.headers.get("msd-channel-id"),
            "msd-request-date-time": request.headers.get("msd-request-date-time"),
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "msd-correlation-id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
