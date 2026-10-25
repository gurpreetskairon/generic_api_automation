import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MBIEDeleteWatchListDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock route for MBIE Watchlist Delete NZBNs API."""
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
        if "nzbns" not in data or not isinstance(data["nzbns"], list):
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": "nzbns field is required and must be an array",
                }
            ), 400

        # Validate NZBN format
        for nzbn in data["nzbns"]:
            if not isinstance(nzbn, str) or not nzbn.isdigit() or len(nzbn) != 13:
                return jsonify(
                    {
                        "httpCode": "400",
                        "messageCode": "MSD-API-E003",
                        "httpMessage": "Bad request",
                        "moreInformation": f"Invalid NZBN format: {nzbn}. Must be 13 digits.",
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

        # Success response - return the remaining NZBNs (simulated)
        remaining_nzbns = ["9429038555189"]  # Simulate some NZBNs remaining
        response_data = {
            "nzbns": remaining_nzbns,
            "links": [
                {
                    "rel": "self",
                    "href": f"/mbie/nzbn/v1/watchlists/{arg}/nzbns",
                    "methods": ["GET"],
                }
            ],
        }

        response_headers = {
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "api-business-govt-nz-Request-Id": request.headers.get("api-business-govt-nz-Request-Id"),
            "api-business-govt-nz-Correlation-Id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 201, response_headers
