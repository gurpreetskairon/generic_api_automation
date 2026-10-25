import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from xml.parsers.expat import ExpatError

import xmltodict

IIB_MARKER = "iib response"
_RESPONSE_KEYS = ("serviceResults", "serviceResult", "service_results")
_CODE_KEYS = ("result", "code", "resultCode", "statusCode")
_SUB_KEYS = ("subResults", "subResult", "subresults")

_SERVICE_FILE_RE = re.compile(r"([^/\\]+?)_test\.py(?:::|$)")
_BATCH_RE = re.compile(r"batch_(\d+)", re.IGNORECASE)
_BYTES_RE = re.compile(r"^b(['\"])(.*)\1$", re.DOTALL)


@dataclass
class TestRecord:
    service: str
    batch: str
    scenario: str
    nodeid: str
    outcome: str
    result_code: str | None = None
    result_message: str | None = None
    sub_result_code: str | None = None
    sub_result_message: str | None = None

    def serialize(self) -> dict:
        return asdict(self)


@dataclass
class ReportSummary:
    created: float | None = None
    duration: float | None = None
    exitcode: int | None = None
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    total: int = 0
    collected: int = 0


def _normalise(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _find_nested(document, key: str):
    if isinstance(document, dict):
        if key in document:
            return document[key]
        for value in document.values():
            found = _find_nested(value, key)
            if found is not None:
                return found
    elif isinstance(document, list):
        for item in document:
            found = _find_nested(item, key)
            if found is not None:
                return found
    return None


def _extract_result_block(block: dict) -> dict[str, str | None]:
    """Extract result_code/result_message/sub-result(optional) from a block

    Args:
        block: A parsed dict resembling a service result element.

    Returns:
        Dictionary with the information of result_code, result_message, sub_result_code
    """
    out: dict[str, str | None] = {
        "result_code": None,
        "result_message": None,
        "sub_result_code": None,
        "sub_result_message": None,
    }

    for key in _CODE_KEYS:
        if key in block and not isinstance(block[key], (dict, list)):
            out["result_code"] = _normalise(block[key])
            break
    for key in ("message", "description"):
        if key in block:
            out["result_message"] = _normalise(block[key])
            break
    if out["result_message"] is None and isinstance(block.get("detail"), str):
        out["result_message"] = _normalise(block["detail"])

    sub_block = None
    for key in _SUB_KEYS:
        if key in block:
            value = block[key]
            sub_block = value[0] if isinstance(value, list) and value else value
            break
    if isinstance(sub_block, dict):
        for key in _CODE_KEYS:
            if key in sub_block and not isinstance(sub_block[key], (dict, list)):
                out["sub_result_code"] = _normalise(sub_block[key])
                break
        for key in ("message", "description"):
            if key in sub_block:
                out["sub_result_message"] = _normalise(sub_block[key])
                break

    return out


def _extract_from_document(document) -> dict[str, str | None]:
    """Locate a service-result block

    Args:
        document: provided information

    Returns:
        needed information used in the report
    """
    service_result = None
    if isinstance(document, dict):
        for key in _RESPONSE_KEYS:
            if key in document:
                value = document[key]
                if isinstance(value, list) and value:
                    service_result = value[0]
                elif isinstance(value, dict):
                    service_result = value
                break
    if service_result is None:
        for key in _RESPONSE_KEYS:
            found = _find_nested(document, key)
            if isinstance(found, list) and found:
                service_result = found[0]
            elif isinstance(found, dict):
                service_result = found
            if service_result is not None:
                break

    if isinstance(service_result, dict):
        info = _extract_result_block(service_result)
        if info["result_code"] is not None or info["result_message"]:
            return info
    return _extract_result_block(service_result) if isinstance(service_result, dict) else {}


def _walk_result_blocks(document):
    if isinstance(document, dict):
        has_identity = "message" in document or any(k in document for k in _CODE_KEYS)
        if has_identity:
            yield document
        for value in document.values():
            yield from _walk_result_blocks(value)
    elif isinstance(document, list):
        for item in document:
            yield from _walk_result_blocks(item)


def _extract_from_document_fallback(document) -> dict[str, str | None]:
    """Extract information for any block carrying a result code/message

    Args:
        document: information provided

    Returns:
        result information
    """
    # best_result: response with result / message / detail key
    # weak_result: response with only code & description
    _BEST_KEYS = ("result", "message", "detail")
    empty = {"result_code": None, "result_message": None, "sub_result_code": None, "sub_result_message": None}
    best_result: dict[str, str | None] = {}
    weak_result: dict[str, str | None] = {}
    for block in _walk_result_blocks(document):
        info = _extract_result_block(block)
        if any(key in block for key in _BEST_KEYS):
            if info["result_code"] is not None and best_result.get("result_code") is None:
                best_result = info
            if info["result_code"] is not None and info["result_message"]:
                return info
        else:
            if info["result_code"] is not None and weak_result.get("result_code") is None:
                weak_result = info
    return best_result if best_result else (weak_result or empty)


def _decode_bytes_repr(content: str) -> str:
    match = _BYTES_RE.match(content)
    if match:
        return match.group(2).encode("utf-8").decode("unicode_escape")
    return content


def _extract_from_content(content: str) -> dict[str, str | None]:
    """Extract result field from an IIB response

    Args:
        content: IIB content information

    Returns:
        information with result fields
    """
    """Extract result fields from a single IIB response body string."""
    empty = {"result_code": None, "result_message": None, "sub_result_code": None, "sub_result_message": None}
    raw = _decode_bytes_repr(content) if content.startswith(("b'", 'b"')) else content

    if raw.startswith(("{", "[")):
        try:
            document = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            document = None
        if document is not None:
            info = _extract_from_document(document)
            if info.get("result_code") is not None or info.get("result_message"):
                return info
            return _extract_from_document_fallback(document)

    try:
        document = xmltodict.parse(raw)
    except (ExpatError, ValueError, TypeError):
        document = None
    if document is not None:
        info = _extract_from_document(document)
        if info.get("result_code") is not None or info.get("result_message"):
            return info
        info = _extract_from_document_fallback(document)
        if info.get("result_code") is not None or info.get("result_message"):
            return info

    info = dict(empty)
    code = re.search(r"<code[^>]*>([^<]+)</code>", raw)
    message = re.search(r"<message[^>]*>([^<]+)</message>", raw)
    if code:
        info["result_code"] = _normalise(code.group(1))
    if message:
        info["result_message"] = _normalise(message.group(1))
    return info


def extract_iib_response(test: dict) -> dict[str, str | None]:
    """Extract the IIB result fields from a single pytest-report test dict

    Args:
        test: One element of an array with tests in the JSON output

    Returns:
        Dictionary with result_code, result_message, sub_result_code, sub_result_message
    """
    empty = {"result_code": None, "result_message": None, "sub_result_code": None, "sub_result_message": None}
    call = test.get("call") or {}
    for log in call.get("log") or []:
        msg = log.get("msg") or ""
        marker_idx = msg.lower().find(IIB_MARKER)
        if marker_idx < 0:
            continue
        content = msg[marker_idx + len(IIB_MARKER + ":"):].strip()
        if not content:
            return empty
        return _extract_from_content(content)
    return empty


def _scrub_outcome(test: dict) -> str:
    """Get outcome information"""
    call = test.get("call") or {}
    return call.get("outcome") or test.get("outcome", "unknown")


def _extract_service_and_batch(nodeid: str) -> tuple[str, str]:
    """Get service and batch information"""
    service = ""
    file_match = _SERVICE_FILE_RE.search(nodeid)
    if file_match:
        service = file_match.group(1)
    if not service:
        service = Path(nodeid.split("::")[0]).stem

    batch = ""
    batch_match = _BATCH_RE.search(nodeid)
    if batch_match:
        batch = f"batch_{batch_match.group(1)}"
    return service, batch


def extract_test_records(report: dict) -> list[TestRecord]:
    """Convert a dictionary of report to a list object

    Args:
        report: input report(report.json)

    Returns:
        list of the test records
    """
    records: list[TestRecord] = []
    for test in report.get("tests") or []:
        nodeid = test.get("nodeid", "")
        service, batch = _extract_service_and_batch(nodeid)
        scenario = nodeid.split("::")[-1] if "::" in nodeid else nodeid
        outcome = _scrub_outcome(test)
        info = extract_iib_response(test)
        records.append(
            TestRecord(
                service=service,
                batch=batch,
                scenario=scenario,
                nodeid=nodeid,
                outcome=outcome,
                result_code=info["result_code"],
                result_message=info["result_message"],
                sub_result_code=info["sub_result_code"],
                sub_result_message=info["sub_result_message"],
            )
        )
    return records


def parse_report(path: Path) -> tuple[list[TestRecord], ReportSummary]:
    """Load and convert a json report file

    Args:
        path: path of the report file

    Returns:
        Tuple of records& summary
    """
    with path.open(encoding="utf-8") as handle:
        report = json.load(handle)

    summary_data = report.get("summary") or {}
    summary = ReportSummary(
        created=report.get("created"),
        duration=report.get("duration"),
        exitcode=report.get("exitcode"),
        passed=summary_data.get("passed", 0),
        failed=summary_data.get("failed", 0),
        skipped=summary_data.get("skipped", 0),
        total=summary_data.get("total", 0),
        collected=summary_data.get("collected", 0),
    )
    return extract_test_records(report), summary
