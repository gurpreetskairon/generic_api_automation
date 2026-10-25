# tests/async_validation/conftest.py
import csv
import json
import os
import re
import warnings
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv

from utils.clients.appinsights_client import AppInsightsClient
from utils.clients.splunk_client import SplunkClient

_THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _THIS_DIR.parents[1]
CALLBACKS_DIR = PROJECT_ROOT / "callbacks"
MANIFEST_CSV = _THIS_DIR / "data" / "async_validations.csv"

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
os.environ.setdefault("ENV", "d11")

_MANIFEST_CACHE = None
_REGISTERED_MARKS = set()


# --------------------------------------------------------------------------
# Manifest: read-only. Built beforehand by build_manifest.py
# --------------------------------------------------------------------------
def _warn_if_manifest_stale():
    """Read-only check, so it is safe under pytest-xdist."""
    if not CALLBACKS_DIR.is_dir():
        return
    csv_mtime = MANIFEST_CSV.stat().st_mtime
    newer = [p.name for p in CALLBACKS_DIR.glob("*.json") if p.stat().st_mtime > csv_mtime]
    if newer:
        warnings.warn(
            f"{len(newer)} callback file(s) are newer than async_validations.csv "
            f"(e.g. {newer[0]}). Re-run tests/async_validation/build_manifest.py "
            f"to include them."
        )


def _load_manifest():
    """Read async_validations.csv (cached per process)."""
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is None:
        if not MANIFEST_CSV.is_file():
            raise FileNotFoundError(
                f"{MANIFEST_CSV} not found. Run "
                f"'python tests/async_validation/build_manifest.py' before pytest."
            )
        _warn_if_manifest_stale()
        with open(MANIFEST_CSV, newline="", encoding="utf-8-sig") as f:
            _MANIFEST_CACHE = list(csv.DictReader(f))
    return _MANIFEST_CACHE


# --------------------------------------------------------------------------
# Marks (same approach as the generic conftest: TEST_ID, SERVICE_CONTRACT, TAGS)
# --------------------------------------------------------------------------
def _sanitize_mark(name: str):
    name = (name or "").strip()
    if not name:
        return None
    name = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if name[0].isdigit():
        name = f"_{name}"
    return name


def _row_tags(data: dict):
    tags = [
        (data.get("TEST_ID") or "").strip(),
        (data.get("SERVICE_CONTRACT") or "").strip(),
    ]
    raw_extra = (data.get("TAGS") or "").strip()
    if raw_extra:
        tags.extend(t.strip() for t in raw_extra.split(",") if t.strip())
    return tags


def _marks_for(config, json_path: Path):
    """Read the callback file's tags and return registered pytest marks."""
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    marks = []
    for tag in _row_tags(data):
        name = _sanitize_mark(tag)
        if not name:
            continue
        if name not in _REGISTERED_MARKS:
            _REGISTERED_MARKS.add(name)
            config.addinivalue_line(
                "markers", f"{name}: auto-generated tag from async callback files"
            )
        marks.append(getattr(pytest.mark, name))
    return marks


# --------------------------------------------------------------------------
# Parametrization: one run of the scenario per row in async_validations.csv
# --------------------------------------------------------------------------
def pytest_generate_tests(metafunc):
    if "async_case" not in metafunc.fixturenames:
        return

    params = []
    ids = []
    for row in _load_manifest():
        json_path = Path(row["JSON_FILE_PATH"])
        marks = _marks_for(metafunc.config, json_path)
        params.append(
            pytest.param({"sr_no": row["SR_NO"], "json_path": json_path}, marks=marks)
        )
        ids.append(f"{row['SR_NO']}-{json_path.stem}")

    metafunc.parametrize("async_case", params, ids=ids, indirect=True)


@pytest.fixture
def async_case(request):
    """{'sr_no': ..., 'json_path': Path(...)} for the current CSV row."""
    return request.param


@pytest.fixture
def callback_data(async_case):
    """The parsed contents of the callback JSON file for the current row."""
    path = async_case["json_path"]
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        pytest.skip(f"Callback file no longer exists: {path}")


@pytest.fixture
def async_result():
    """Scratch dict the steps use to pass fetched responses to each other."""
    return {}


def pytest_bdd_before_scenario(request, feature, scenario):
    """Allure dynamic title (same reason as in the generic conftest: must be a bdd hook)."""
    try:
        data = request.getfixturevalue("callback_data")
    except Exception:
        return

    title_parts = [
        (data.get("TEST_ID") or "").strip(),
        (data.get("SERVICE_CONTRACT") or "").strip(),
        (data.get("CONDITION") or "").strip(),
    ]
    title_parts = [p for p in title_parts if p]
    if title_parts:
        allure.dynamic.title(" - ".join(title_parts))


# --------------------------------------------------------------------------
# Log-source clients (session scoped: created lazily, logged in once)
# --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def splunk_client(playwright):
    client = SplunkClient(playwright)
    yield client
    client.close()


@pytest.fixture(scope="session")
def appinsights_client():
    client = AppInsightsClient()
    yield client
    client.close()
