from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition
from utils.api_utils.mock_server.constants import (
    EMPLOYER_PUBLISH_BAD_REQUEST,
    EMPLOYER_PUBLISH_SUCCESS,
)


class MSDPublishEmployerEventDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock endpoint for publishing employer events."""
        data = request.get_json()

        # Check for missing required fields
        if not data or "businessName" not in data:
            return jsonify(EMPLOYER_PUBLISH_BAD_REQUEST["body"]), EMPLOYER_PUBLISH_BAD_REQUEST["status"]

        # Check for missing required headers
        required_headers = [
            "transactionId",
            "requestDateTime",
            "sourceEventType",
            "sourceSystem",
        ]
        missing_headers = [header for header in required_headers if header not in request.headers]

        if missing_headers:
            return jsonify(
                {
                    "serviceResults": [
                        {
                            "result": "400",
                            "message": f"Missing required headers: {', '.join(missing_headers)}",
                            "resultDescription": "Bad Request",
                        }
                    ]
                }
            ), 400

        # Return success response
        response_headers = EMPLOYER_PUBLISH_SUCCESS["headers"]
        return "", EMPLOYER_PUBLISH_SUCCESS["status"], response_headers
