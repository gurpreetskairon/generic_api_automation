"""
Builds tests/async_validation/data/async_validations.csv from the JSON files
in <project_root>/callbacks.

Can be used two ways:
    - imported:    build_manifest()   (called by conftest.py before parametrization)
    - standalone:  python tests/async_validation/build_manifest.py
"""
import csv
import json
import os
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CALLBACKS_DIR = os.getenv("CALLBACKS_DIR", PROJECT_ROOT / "callbacks")
OUTPUT_CSV = PROJECT_ROOT / "tests" / "async_validation" / "data" / "async_validations.csv"
OUTPUT_COLUMNS = ["SR_NO", "JSON_FILE_PATH"]


def build_manifest() -> list[dict]:
    """
    Scan the callbacks folder, write the manifest CSV and return its rows
    as a list of dicts: [{"SR_NO": "1", "JSON_FILE_PATH": "..."}, ...]
    """
    if not CALLBACKS_DIR.is_dir():
        raise FileNotFoundError(f"callbacks folder not found: {CALLBACKS_DIR}")

    json_files = sorted(CALLBACKS_DIR.glob("*.json"), key=lambda p: p.name.lower())
    if not json_files:
        print(f"WARNING: no .json files found in {CALLBACKS_DIR}")

    valid_paths = []
    for path in json_files:
        # Sanity check only: skip files the validation run would choke on
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARNING: skipping unreadable/invalid JSON {path.name}: {exc}")
            continue
        if not (data.get("APIM_UUID") or data.get("IIB_UUID")):
            print(f"WARNING: {path.name} has no APIM_UUID/IIB_UUID, skipping")
            continue
        valid_paths.append(str(path.resolve()))

    rows = [
        {"SR_NO": str(sr_no), "JSON_FILE_PATH": full_path}
        for sr_no, full_path in enumerate(valid_paths, start=1)
    ]

    # Write to a temp file then swap it in, so a reader (e.g. another pytest-xdist
    # worker) never sees a half-written CSV.
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=OUTPUT_CSV.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_name, OUTPUT_CSV)
    except Exception:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
        raise

    print(f"Wrote {len(rows)} row(s) to {OUTPUT_CSV}")
    return rows


if __name__ == "__main__":
    try:
        build_manifest()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
