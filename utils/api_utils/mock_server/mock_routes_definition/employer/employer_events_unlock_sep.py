from flask import jsonify

from utils.api_utils.mock_server.base import RoutesDefinition
from utils.api_utils.mock_server.constants import (
    SEP_MESSAGE_NOT_FOUND,
    SEP_MESSAGE_UNLOCKED,
)


class EmployerEventsUnlockSepDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock endpoint for unlocking SEP event messages."""
        if arg == "invalid-message-id":
            return jsonify(SEP_MESSAGE_NOT_FOUND["body"]), SEP_MESSAGE_NOT_FOUND["status"]

        return "", SEP_MESSAGE_UNLOCKED["status"]
