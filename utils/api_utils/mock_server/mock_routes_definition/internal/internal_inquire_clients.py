from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition
from utils.api_utils.mock_server.common import (
    get_client_profile_headers,
    validate_client_profile_headers,
)


class InternalInquireClientsDefinition(RoutesDefinition):
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

        client_numbers = request.args.get("clientNumbers")
        flt_token = request.args.get("fltToken")
        privacy_domain = request.args.get("privacyDomain")

        # FLT token validation
        if flt_token:
            if not privacy_domain:
                return (
                    jsonify(
                        {
                            "serviceResults": [
                                {
                                    "result": "API-400",
                                    "message": "Privacy domain is required when using FLT token",
                                    "resultDescription": "Bad Request",
                                }
                            ]
                        }
                    ),
                    400,
                    get_client_profile_headers(),
                )

            # Simulate FLT token not found
            if flt_token == "InvalidFlt":
                return (
                    jsonify(
                        {
                            "serviceResults": [
                                {
                                    "result": "API-404",
                                    "message": "FLT token not found or invalid",
                                    "resultDescription": "Not Found",
                                }
                            ]
                        }
                    ),
                    404,
                    get_client_profile_headers(),
                )

            # Success response for FLT token
            return (
                jsonify(
                    {
                        "participants": [
                            {
                                "identities": [
                                    {
                                        "identifier": "987654321",
                                        "type": {
                                            "code": "CLIENTNUMBER",
                                            "description": "Client Number",
                                        },
                                    }
                                ]
                            }
                        ]
                    }
                ),
                200,
                get_client_profile_headers(),
            )

        # Client numbers validation
        if client_numbers:
            clients = client_numbers.split(",")
            participants = []

            for client_num in clients:
                client_num = client_num.strip()
                if client_num.isdigit():
                    participants.append(
                        {
                            "identities": [
                                {
                                    "identifier": client_num,
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
                                    "fullName": "David Wilson",
                                }
                            ],
                        }
                    )

            return (
                jsonify({"participants": participants}),
                200,
                get_client_profile_headers(),
            )

        # No valid parameters provided
        return (
            jsonify(
                {
                    "serviceResults": [
                        {
                            "result": "API-400",
                            "message": "Please provide clientNumbers or fltToken with privacyDomain",
                            "resultDescription": "Bad Request",
                        }
                    ]
                }
            ),
            400,
            get_client_profile_headers(),
        )
