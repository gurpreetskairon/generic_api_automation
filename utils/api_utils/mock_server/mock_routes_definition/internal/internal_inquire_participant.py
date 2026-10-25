from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition
from utils.api_utils.mock_server.common import (
    get_client_profile_headers,
    validate_client_profile_headers,
)


class InternalInquireParticipantDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        # Validate headers
        header_validation = validate_client_profile_headers()
        if header_validation:
            return (
                jsonify(header_validation[0]),
                header_validation[1],
                get_client_profile_headers(),
            )

        # Validate authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return (
                jsonify(
                    {
                        "serviceResults": [
                            {
                                "result": "API-401",
                                "message": "Invalid or missing authentication credentials",
                                "resultDescription": "Unauthorized",
                            }
                        ]
                    }
                ),
                401,
                get_client_profile_headers(),
            )

        # Check for invalid participant ID format
        if not arg.isdigit() or len(arg) < 8:
            return (
                jsonify(
                    {
                        "serviceResults": [
                            {
                                "result": "API-400",
                                "message": "Invalid participant ID format",
                                "resultDescription": "Bad Request",
                            }
                        ]
                    }
                ),
                400,
                get_client_profile_headers(),
            )

        # Simulate participant not found
        if arg == "99999999":
            return (
                jsonify(
                    {
                        "serviceResults": [
                            {
                                "result": "API-404",
                                "message": "The participant with the provided ID does not exist",
                                "resultDescription": "Not Found",
                                "objectRef": {
                                    "type": "PARTICIPANT",
                                    "value": arg,
                                },
                            }
                        ]
                    }
                ),
                404,
                get_client_profile_headers(),
            )

        # Success response with participant data
        client_data = {
            "participant": {
                "identities": [
                    {
                        "identifier": arg,
                        "type": {
                            "code": "CLIENTNUMBER",
                            "description": "Client Number",
                        },
                    }
                ],
                "dateOfBirth": "1980-01-01",
                "names": [
                    {
                        "lastName": "Wilson",
                        "firstName": "David",
                        "middleName": "John",
                        "title": "Mr",
                        "fullName": "David John Wilson",
                        "period": {"start": "2020-01-01", "end": "2025-05-16"},
                        "type": {"code": "LEGAL", "description": "Legal Name"},
                    }
                ],
            }
        }

        return jsonify(client_data), 200, get_client_profile_headers()
