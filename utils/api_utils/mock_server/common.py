import uuid

from flask import request


def get_client_profile_headers():
    """Generate common response headers for Client Profile Management API."""
    return {
        "transactionId": request.headers.get("transactionId", str(uuid.uuid4())),
        "correlationId": request.headers.get("correlationId", str(uuid.uuid4())),
        "requestDateTime": request.headers.get("requestDateTime"),
        "Content-Type": "application/json",
    }


def validate_client_profile_headers():
    """Validate required headers for Client Profile Management API."""
    required_headers = [
        "transactionId",
        "sourceSystem",
        "requestDateTime",
        "apimSubscriptionKey",
    ]
    missing_headers = []

    for header in required_headers:
        if header not in request.headers:
            missing_headers.append(header)

    if missing_headers:
        return {
            "serviceResults": [
                {
                    "result": "API-400",
                    "message": f"Missing required headers: {', '.join(missing_headers)}",
                    "resultDescription": "Bad Request",
                }
            ]
        }, 400

    # Validate UUID format for transactionId
    try:
        uuid.UUID(request.headers.get("transactionId"))
    except (ValueError, TypeError):
        return {
            "serviceResults": [
                {
                    "result": "API-400",
                    "message": "transactionId must be a valid UUID format",
                    "resultDescription": "Bad Request",
                }
            ]
        }, 400

    # Validate datetime format for requestDateTime
    request_datetime = request.headers.get("requestDateTime")
    if not request_datetime or "T" not in request_datetime:
        return {
            "serviceResults": [
                {
                    "result": "API-400",
                    "message": "requestDateTime must be in ISO-8601 format",
                    "resultDescription": "Bad Request",
                }
            ]
        }, 400

    return None
