import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class MBIEGetWatchListDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock route for MBIE Watchlist NZBNs API."""
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

        # Success response
        response_data = {
            "nzbns": ["9429038555189", "9429039467291", "9429040123456"],
            "links": [
                {
                    "rel": "self",
                    "href": f"/mbie/nzbn/v1/watchlists/{arg}/nzbns",
                    "methods": ["GET"],
                },
                {
                    "rel": "append",
                    "href": f"/mbie/nzbn/v1/watchlists/{arg}/action-append-nzbns",
                    "methods": ["POST"],
                },
            ],
        }

        response_headers = {
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "api-business-govt-nz-Request-Id": request.headers.get("api-business-govt-nz-Request-Id"),
            "api-business-govt-nz-Correlation-Id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
