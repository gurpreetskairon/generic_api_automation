import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MSDCheckConnectivityDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Handle connectivity check requests."""
        # Validate API key
        if "ocp-apim-subscription-key" not in request.headers:
            return jsonify(
                {
                    "httpCode": "401",
                    "messageCode": "MSD-API-E013",
                    "httpMessage": "Unauthorized",
                    "moreInformation": "Provider Error: Access denied due to a missing application credentials or subscription key. Make sure to include an application token or a subscription key when making requests to the API.",
                }
            ), 401

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

        # Success response
        name = request.args.get("name", "")
        response_data = {"message": f"Hello {name}, APIM api is up and running"}

        response_headers = {
            "msd-channel-id": request.headers.get("msd-channel-id"),
            "msd-request-date-time": request.headers.get("msd-request-date-time"),
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "msd-correlation-id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
