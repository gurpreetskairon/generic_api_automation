"""
async_callback.py

Writes one JSON "callback" file per async-contract test run, capturing
everything a later, separate script needs to look the real response up
in Splunk (IIB) or Azure Application Insights (APIM), validate it against
the ASYNC_* expectations, and then delete the file.

CALLBACK_FOLDER must be set in .env — the directory these files are
written to and later consumed from.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


def get_callback_dir() -> Path:
    callback_dir = os.getenv("CALLBACK_DIR")
    if not callback_dir:
        raise ValueError("CALLBACK_DIR is not set in .env")
    path = Path(callback_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _sanitize_for_filename(value: str) -> str:
    return re.sub(r"[^0-9a-zA-Z_-]", "_", (value or "").strip())


def build_callback_filename(test_id: str, service_contract: str) -> str:
    # Microsecond precision, no separators that are invalid in Windows
    # filenames (":" in particular) — safe even for back-to-back reruns.
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{_sanitize_for_filename(test_id)}_{_sanitize_for_filename(service_contract)}_{timestamp}.json"


def write_callback_file(testcase_row: dict, api_context) -> Path:
    """
    Called right after the request has been sent (both legs, if this is a
    comparison run) and before the ack's own status/body assertions run.
    Everything read here was already set by the "I fetch the endpoint" and
    "the request information" steps.
    """
    is_comparison = api_context.is_comparison

    record = {
        "TEST_ID": testcase_row.get("TEST_ID", ""),
        "SERVICE_CONTRACT": testcase_row.get("SERVICE_CONTRACT", ""),
        "TAGS": testcase_row.get("TAGS", ""),
        "CONDITION": testcase_row.get("CONDITION", ""),
        "TEST_TYPE": os.getenv("TEST_TYPE", ""),
        "APIM_ENDPOINT": api_context.apim.base_url + api_context.apim.endpoint,
        "IIB_ENDPOINT": (api_context.iib.base_url + api_context.iib.endpoint) if is_comparison else "",
        "APIM_HEADERS": getattr(api_context.apim, "headers", None),
        "IIB_HEADERS": getattr(api_context.iib, "headers", None) if is_comparison else "",
        "APIM_QUERY_PARAMS": getattr(api_context.apim, "query_params", None),
        "IIB_QUERY_PARAMS": getattr(api_context.iib, "query_params", None) if is_comparison else "",
        "APIM_REQUEST_BODY": getattr(api_context.apim, "request_body", None),
        "IIB_REQUEST_BODY": getattr(api_context.iib, "request_body", None) if is_comparison else "",
        "APIM_UUID": testcase_row.get("APIM_UUID"),
        "IIB_UUID": testcase_row.get("IIB_UUID") if is_comparison else testcase_row.get("APIM_UUID"),
        "ASYNC_COMPARISON_TO_IGNORE": testcase_row.get("ASYNC_COMPARISON_TO_IGNORE", ""),
        "ASYNC_RESPONSE_CODE": testcase_row.get("ASYNC_RESPONSE_CODE", ""),
        "ASYNC_VALIDATE_DATA": testcase_row.get("ASYNC_VALIDATE_DATA", ""),
    }

    callback_dir = get_callback_dir()
    file_path = callback_dir / build_callback_filename(record["TEST_ID"], record["SERVICE_CONTRACT"])
    file_path.write_text(json.dumps(record, indent=2, default=str), encoding="utf-8")
    return file_path
