"""
Header Types:
Header_A  - SOAP XML  ``text/xml; charset=utf-8``  (no SOAPAction)
Header_B  - SOAP XML  ``text/xml``  (no charset, no SOAPAction)
Header_C  - SOAP XML  ``application/xml``  +  ``MSD-Sub-Env``
Header_D  - SOAP XML  ``application/xml``  only  (no MSD-Sub-Env)
Header_E  - SOAP XML  with ``SOAPAction`` routing header
Header_F  - REST      ``Authorization: Basic``  only  (no Content-Type)
Header_G  - REST JSON ``application/json``  +  ``Authorization: Basic``
Header_H  - REST JSON ``application/json``  +  ``Authorization: Basic``  +  ``MSD-Sub-Env``
Header_I  - STAR      ``transactionId``  +  ``sourceSystem``  +  ``securityTokenId``
Header_J  - Custom    service-specific header sets  (SC157, SC550)
Header_K  - REST JSON ``application/json``  +  ``Authorization: Basic``  +  ``Accept``  +  ``MSD-Sub-Env``
"""

from __future__ import annotations
import ast
import csv
import json
import re
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, cast


# for json output file
class EndpointMetadata(TypedDict):
    version: int
    generated_at: str
    headers: dict[str, str]
    batches: dict[str, str]
    http_methods: dict[str, str]


# scan folders
_REPO_ROOT = Path(__file__).resolve().parents[2]
_BATCH_BASE = _REPO_ROOT / "tests" / "api_test" / "soap_api" / "comparison_testing"
_PAYLOAD_DIR = _REPO_ROOT / "apps" / "services" / "integration_soap" / "payload_data"
_PAYLOAD_SETUP_FILE = _REPO_ROOT / "utils" / "api_utils" / "helper" / "payload_setup.py"

# target output
_ENDPOINTS_CSV = _REPO_ROOT / "service_contract_data" / "ENDPOINTS.csv"
_JSON_OUTPUT = _REPO_ROOT / "utils" / "sqlite" / "endpoints_metadata.json"

_METADATA_VERSION = 1

# columns for metadata
_CSV_TARGET_COLUMNS: tuple[str, ...] = ("HTTP_METHOD", "HEADER", "BATCH")

_HeaderPredicate = Callable[[dict[str, str]], bool]

_HEADER_RULES: list[tuple[str, _HeaderPredicate]] = [
    # J: Custom — action + correlationId, or auditId without securityTokenId.
    ("Header_J", lambda h: ("action" in h and "correlationid" in h) or ("auditid" in h and "securitytokenid" not in h)),
    # I: STAR — transactionId + sourceSystem + securityTokenId.
    ("Header_I", lambda h: "transactionid" in h and "sourcesystem" in h and "securitytokenid" in h),
    # A: text/xml; charset — Content-Type takes precedence over SOAPAction.
    ("Header_A", lambda h: h.get("content-type", "").startswith("text/xml") and "charset" in h.get("content-type", "")),
    # K: Accept + Basic Auth + MSD-Sub-Env — checked before Header_H.
    ("Header_K", lambda h: "accept" in h and "authorization" in h and "msd-sub-env" in h),
    # H: JSON + Basic Auth + MSD-Sub-Env.
    ("Header_H", lambda h: h.get("content-type") == "application/json" and "authorization" in h and "msd-sub-env" in h),
    # G: JSON + Basic Auth.
    ("Header_G", lambda h: h.get("content-type") == "application/json" and "authorization" in h),
    # F: REST Basic Auth only.
    ("Header_F", lambda h: "authorization" in h and "content-type" not in h),
    # E: SOAP with SOAPAction.
    ("Header_E", lambda h: "soapaction" in h),
    # C: application/xml + MSD-Sub-Env.
    ("Header_C", lambda h: h.get("content-type") == "application/xml" and "msd-sub-env" in h),
    # D: application/xml only.
    ("Header_D", lambda h: h.get("content-type") == "application/xml"),
    # B: text/xml (no charset).
    ("Header_B", lambda h: h.get("content-type", "").startswith("text/xml"))
]

# Http header keys used in the code
_HEADER_KEYS = frozenset(
    {
        "content-type",
        "soapaction",
        "authorization",
        "msd-sub-env",
        "transactionid",
        "sourcesystem",
        "securitytokenid",
        "auditid",
        "accept",
        "action",
        "correlationid",
        "msd-a2c-bypass",
        "securitytokentype",
        "interactionpattern",
        "callbackaddress",
        "messagetype",
        "requestdatetime"
    }
)

_VALUE_SENSITIVE_KEYS = frozenset({"content-type"})
_SC_RE = re.compile(r"((?:sc|dp)\d+)(?:_?v\d+)?", re.IGNORECASE)
_SEND_RE = re.compile(r"send_(?:rest_)?(post|get|put)_request", re.IGNORECASE)
_REQUIRED_SECTIONS = frozenset({"headers", "batches", "http_methods"})


# helpers
def _normalise_sc(raw: str) -> str:
    return raw.upper().replace("_V", "V")


def _sc_from_filename(filename: str) -> str | None:
    m = _SC_RE.match(Path(filename).stem)
    return _normalise_sc(m.group(0)) if m else None


def _upper_map(raw: dict[str, str]) -> dict[str, str]:
    return {k.upper(): v for k, v in raw.items()}


# scan comparison testing folder
def build_batch_map() -> dict[str, str]:
    result: dict[str, str] = {}
    if not _BATCH_BASE.exists():
        return result

    for batch_dir in sorted(_BATCH_BASE.iterdir()):
        m = re.match(r"batch_(\d+)", batch_dir.name, re.IGNORECASE)
        if not m or not batch_dir.is_dir():
            continue
        label = f"Batch-{int(m.group(1))}"
        steps = batch_dir / "steps_def"
        if not steps.exists():
            continue
        for f in sorted(steps.glob("*_test.py")):
            sc = _sc_from_filename(f.name)
            if sc:
                result[sc] = label
    return result


# scan payload_data folder
def build_header_map(batch_map: dict[str, str] | None = None) -> dict[str, str]:
    header_map: dict[str, str] = {}

    if _PAYLOAD_DIR.exists():
        for py in sorted(_PAYLOAD_DIR.rglob("*.py")):
            if py.name.startswith("_") or py.parent.name == "__pycache__":
                continue
            sc = _sc_from_filename(py.name)
            if not sc:
                continue
            keys = _ast_extract_headers(py.read_text(encoding="utf-8"))
            if keys:
                header_map[sc] = _classify_header(keys)

    if _PAYLOAD_SETUP_FILE.exists():
        by_func = _ast_extract_headers_by_function(_PAYLOAD_SETUP_FILE.read_text(encoding="utf-8"))
        for func_name, keys in sorted(by_func.items()):
            sc = _sc_from_filename(func_name)
            if sc and sc not in header_map:
                header_map[sc] = _classify_header(keys)

    if _BATCH_BASE.exists():
        for batch_dir in sorted(_BATCH_BASE.iterdir()):
            if not batch_dir.is_dir():
                continue
            steps = batch_dir / "steps_def"
            if not steps.exists():
                continue
            for f in sorted(steps.glob("*_test.py")):
                sc = _sc_from_filename(f.name)
                if not sc or sc in header_map:
                    continue
                keys = _ast_extract_headers(f.read_text(encoding="utf-8"))
                if keys:
                    header_map[sc] = _classify_header(keys)

    # cross-check to ensure that no services are missing from the CSV file
    if _ENDPOINTS_CSV.exists():
        with open(_ENDPOINTS_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                sc = _normalise_sc(row.get("SERVICE_CONTRACT", "").strip())
                hdr = row.get("HEADER", "").strip()
                if sc and hdr and sc not in header_map:
                    header_map[sc] = hdr

    # for the services with different versions
    if batch_map:
        for batch_sc in batch_map:
            if batch_sc in header_map:
                continue
            base_m = re.match(r"([A-Z]+\d+)[Vv]", batch_sc)
            if base_m and base_m.group(1) in header_map:
                header_map[batch_sc] = header_map[base_m.group(1)]

    return header_map


# scan comparison testing folder to get the http method
def build_http_method_map() -> dict[str, str]:
    result: dict[str, str] = {}
    if not _BATCH_BASE.exists():
        return result

    for batch_dir in sorted(_BATCH_BASE.iterdir()):
        if not batch_dir.is_dir():
            continue
        steps = batch_dir / "steps_def"
        if not steps.exists():
            continue
        for f in sorted(steps.glob("*_test.py")):
            sc = _sc_from_filename(f.name)
            if not sc:
                continue
            methods = set(_SEND_RE.findall(f.read_text(encoding="utf-8")))
            if methods:
                result[sc] = "POST" if "post" in methods else "GET" if "get" in methods else "PUT"
    return result


# build up the header key-value in a dic
def _snapshot_from_dict_node(node: ast.Dict) -> dict[str, str] | None:
    snap: dict[str, str] = {}
    for kn, vn in zip(node.keys, node.values):
        if not (isinstance(kn, ast.Constant) and isinstance(kn.value, str)):
            continue
        k = kn.value.lower()
        if k not in _HEADER_KEYS:
            continue
        if k in _VALUE_SENSITIVE_KEYS and isinstance(vn, ast.Constant) and isinstance(vn.value, str):
            snap[k] = vn.value.lower()
        else:
            snap[k] = ""
    return snap or None


# get headers key from the dic
def _header_snapshots_in(tree: ast.AST) -> list[dict[str, str]]:
    snapshots: list[dict[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            snap = _snapshot_from_dict_node(node)
            if snap is not None:
                snapshots.append(snap)
    return snapshots


# get the first key-value
def _pick_first_snapshot(snapshots: list[dict[str, str]]) -> dict[str, str]:
    for snap in snapshots:
        if "content-type" in snap:
            return snap
    return snapshots[0] if snapshots else {}


# parse the source
def _parse(source: str) -> ast.AST | None:
    try:
        return ast.parse(source)
    except SyntaxError:
        return None


# pick up the key-value from the source
def _ast_extract_headers(source: str) -> dict[str, str]:
    tree = _parse(source)
    if tree is None:
        return {}
    return _pick_first_snapshot(_header_snapshots_in(tree))


# extract headers from payload_setup
def _ast_extract_headers_by_function(source: str) -> dict[str, dict[str, str]]:
    tree = _parse(source)
    if tree is None:
        return {}
    result: dict[str, dict[str, str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            snapshots = _header_snapshots_in(node)
            if snapshots:
                result[node.name] = _pick_first_snapshot(snapshots)
    return result


# classify the header's group
def _classify_header(keys: dict[str, str]) -> str:
    for label, pred in _HEADER_RULES:
        if pred(keys):
            return label
    return "Header_A"


# export the JSON file
def collect_metadata() -> EndpointMetadata:
    print("Scanning batch folders ...")
    batches = build_batch_map()
    print(f"  {len(batches)} SCs across {len(set(batches.values()))} batches")

    print("Scanning payload_data headers ...")
    headers = build_header_map(batches)
    print(f"  {len(headers)} header classifications")

    print("Scanning test files for HTTP methods ...")
    http_methods = build_http_method_map()
    print(f"  {len(http_methods)} HTTP method mappings")

    _report_gaps(batches, headers)

    return {
        "version": _METADATA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "headers": headers,
        "batches": batches,
        "http_methods": http_methods
    }


def export_metadata(metadata: EndpointMetadata, output_path: Path = _JSON_OUTPUT) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metadata, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return output_path


def _report_gaps(batch_map: dict[str, str], header_map: dict[str, str]) -> None:
    if missing := sorted(set(batch_map) - set(header_map)):
        print(f"  WARNING: In batch folders but no header classification: {missing}")
    if orphan := sorted(set(header_map) - set(batch_map)):
        print(f"  WARNING: Header classification but not in any batch: {orphan}")


# load metadata and prepare to update the csv file
def load_metadata(json_path: Path) -> EndpointMetadata:
    if not json_path.exists():
        raise SystemExit(f"Metadata JSON not found: {json_path}\nRun 'export' first.")

    try:
        raw: object = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {json_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise SystemExit(f"{json_path}: top-level JSON value must be an object.")

    if missing := sorted(_REQUIRED_SECTIONS - raw.keys()):
        raise SystemExit(f"{json_path}: missing required sections {missing}. Re-run 'export'.")

    if malformed := [s for s in sorted(_REQUIRED_SECTIONS) if not isinstance(raw[s], dict)]:
        raise SystemExit(f"{json_path}: sections must be string-keyed objects: {malformed}")

    return cast(EndpointMetadata, raw)


# update metadata columns in the csv file
def update_endpoints_csv(metadata: EndpointMetadata, csv_path: Path = _ENDPOINTS_CSV) -> None:
    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

    lookup = {
        "HTTP_METHOD": _upper_map(metadata["http_methods"]),
        "HEADER": _upper_map(metadata["headers"]),
        "BATCH": _upper_map(metadata["batches"])
    }

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    for col in _CSV_TARGET_COLUMNS:
        if col not in fieldnames:
            fieldnames.append(col)

    changes: list[tuple[str, str, str]] = []
    touched_rows = 0

    for row in rows:
        sc_key = row.get("SERVICE_CONTRACT", "").strip().upper()
        modified = False
        for col, mapping in lookup.items():
            if row.get(col, "").strip():
                continue
            new_val = mapping.get(sc_key)
            if new_val:
                changes.append((row["SERVICE_CONTRACT"], col, new_val))
                row[col] = new_val
                modified = True
        if modified:
            touched_rows += 1

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {csv_path.name}: {touched_rows} rows, {len(changes)} cell changes.")
    for col in _CSV_TARGET_COLUMNS:
        count = sum(1 for c in changes if c[1] == col)
        if count:
            print(f"  {col}: +{count}")


def update_metadata() -> None:
    metadata = collect_metadata()
    output = export_metadata(metadata)
    counts = (len(metadata["headers"]), len(metadata["batches"]), len(metadata["http_methods"]))
    print(
        f"Exported metadata (headers: {counts[0]}, batches: {counts[1]}, "
        f"methods: {counts[2]}) -> {output.relative_to(_REPO_ROOT)}"
    )

    update_endpoints_csv(metadata)


if __name__ == "__main__":
    update_metadata()
