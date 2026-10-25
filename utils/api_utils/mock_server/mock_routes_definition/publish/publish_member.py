import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class PublishMemberDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock route for Provider Member Publish API."""
        data = request.json  # Validate required fields
        required_fields = ["providerMemberExternalID", "name", "role", "status"]
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

        # Simulate invalid providerMemberExternalID
        if data and data.get("providerMemberExternalID") == "INVALID":
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E003",
                    "httpMessage": "Bad request",
                    "moreInformation": "The provided providerMemberExternalID is invalid.",
                }
            ), 400  # Success response
        response_data = {"status": "success"}
        response_headers = {
            "msd-channel-id": request.headers.get("msd-channel-id"),
            "msd-request-date-time": request.headers.get("msd-request-date-time"),
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "msd-correlation-id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
