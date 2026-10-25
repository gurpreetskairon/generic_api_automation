import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MBIESendNotificationDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock route for MBIE Watchlist Send Test Notification API."""
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

        data = request.json
        if not data:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": "Request body is required",
                }
            ), 400

        # Validate required fields
        if "text" not in data:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": "text field is required",
                }
            ), 400

        # Simulate not found scenario
        if arg == "INVALID":
            return jsonify(
                {
                    "httpCode": "404",
                    "messageCode": "MSD-API-E031",
                    "httpMessage": "Resource not found",
                    "moreInformation": "Watchlist not found",
                }
            ), 404

        # Success response - echo back the test message
        response_data = {"text": data["text"]}

        response_headers = {
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "api-business-govt-nz-Request-Id": request.headers.get("api-business-govt-nz-Request-Id"),
            "api-business-govt-nz-Correlation-Id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 201, response_headers
