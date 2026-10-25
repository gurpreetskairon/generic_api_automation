from flask import jsonify

from utils.api_utils.mock_server.base import RoutesDefinition
from utils.api_utils.mock_server.constants import (
    SEP_INVALID_SUBSCRIPTION,
    SEP_MESSAGE_SUCCESS,
    SEP_NO_MESSAGES,
)


class EmployerEventsConsumeSepDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock endpoint for consuming SEP event messages."""
        if arg == "invalid-subscription":
            return jsonify(SEP_INVALID_SUBSCRIPTION["body"]), SEP_INVALID_SUBSCRIPTION["status"]

        if arg == "empty-subscription":
            return "", SEP_NO_MESSAGES["status"]

        # Return success response with message
        response_headers = SEP_MESSAGE_SUCCESS["headers"]
        return (
            jsonify(SEP_MESSAGE_SUCCESS["body"]),
            SEP_MESSAGE_SUCCESS["status"],
            response_headers,
        )
