import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MSDLinkAccountsDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Handle participant account linking requests."""
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

        data = request.json
        if not data:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": "Request body is required",
                }
            ), 400  # Validate required fields
        required_fields = [
            "referenceNumber",
            "flt",
            "privacyDomain",
            "idp",
            "referenceTypeCode",
        ]
        if data:
            missing_fields = [field for field in required_fields if field not in data]
        else:
            missing_fields = required_fields
        if missing_fields:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": f"Missing required fields: {', '.join(missing_fields)}",
                }
            ), 400

        # Validate field lengths
        if len(data["referenceNumber"]) > 18:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E003",
                    "httpMessage": "Bad request",
                    "moreInformation": "referenceNumber exceeds maximum length of 18 characters",
                }
            ), 400

        # Success response
        response_data = {
            "message": "Successfully linked FLT to participant account",
            "referenceNumber": data["referenceNumber"],
            "fltID": data["flt"],
        }

        response_headers = {
            "msd-channel-id": request.headers.get("msd-channel-id"),
            "msd-request-date-time": request.headers.get("msd-request-date-time"),
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "msd-correlation-id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
