import uuid

from flask import jsonify, request

from utils.api_utils.mock_server.base import RoutesDefinition


class WekaContractDetailsDefinition(RoutesDefinition):
    def create_routes_def(self, arg):
        """Mock route for WEKA Contract Details API."""
        weka_supplier_id = request.args.get("WEKASupplierId")
        contract_number = request.args.get("ContractNumber")

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

        # Validate required parameters
        if not weka_supplier_id or not contract_number:
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E001",
                    "httpMessage": "Bad request",
                    "moreInformation": "Both WEKASupplierId and ContractNumber are required.",
                }
            ), 400

        # Simulate invalid contract number
        if contract_number == "INVALID":
            return jsonify(
                {
                    "httpCode": "400",
                    "messageCode": "MSD-API-E003",
                    "httpMessage": "Bad request",
                    "moreInformation": "The provided ContractNumber is invalid.",
                }
            ), 400

        # Success response with exact schema match
        response_data = {
            "contractDetails": {
                "WEKASupplierId": weka_supplier_id,
                "ContractNumber": contract_number,
                "ContractId": 300000060834494,
                "Lines": [
                    {
                        "ServiceCode": "FVRESP",
                        "ContractLineItemName": "Other responses for people experiencing family violence",
                        "ContractLineItemNumber": "2134566445666",
                        "StartDate": "2024-01-01",
                        "EndDate": "2025-12-31",
                        "LineQuantity": 1,
                    }
                ],
            }
        }

        response_headers = {
            "msd-channel-id": request.headers.get("msd-channel-id"),
            "msd-request-date-time": request.headers.get("msd-request-date-time"),
            "msd-transaction-id": request.headers.get("msd-transaction-id"),
            "msd-correlation-id": str(uuid.uuid4()),
        }

        return jsonify(response_data), 200, response_headers
