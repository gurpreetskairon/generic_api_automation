import os
import csv
import re
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv

from utils.api.api_context import APIContext
from utils.comparison.payload_resolver import resolve_payload, parse_validate_data, _is_inline_payload
from utils.helpers.dynamic_tokens import resolve_row_tokens

# --------------------------------------------------------------------------
# Load .env first, before any fixtures are defined
# --------------------------------------------------------------------------
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


# conftest.py (project root, or the one above tests/steps/)

# Importing these triggers their @register_token decorators as a side
# effect — even though nothing here calls the functions directly.
import utils.helpers.date_util          # registers resolve_date_token
import utils.helpers.helper            # registers generate_uuid (adjust path to wherever it actually lives)


# --------------------------------------------------------------------------
# CLI options: --env and --test-type override .env values if passed
# --------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None,
                      help="Override the ENV value from .env (e.g. --env u10)")
    parser.addoption("--test-type", action="store", default=None,
                      help="Override the TEST_TYPE value from .env (e.g. --test-type integration)")
    parser.addoption("--apim-as-iib", action="store_true", default=False,
                      help="Point the APIM base URL at the IIB base URL (useful when you want "
                           "the 'APIM' slot to actually hit IIB, e.g. for baseline/sanity runs)")

def _row_tags(row):
    """All raw tag strings for a row: TEST_ID, SERVICE_CONTRACT, plus any
    comma-separated values in the TAGS column."""
    tags = [
        (row.get("TEST_ID") or "").strip(),
        (row.get("SERVICE_CONTRACT") or "").strip(),
    ]
    raw_extra = (row.get("TAGS") or "").strip()
    if raw_extra:
        tags.extend(t.strip() for t in raw_extra.split(",") if t.strip())
    print(f"tags: {tags}")
    return tags

def pytest_configure(config):
    cli_env = config.getoption("--env")
    if cli_env:
        os.environ["ENV"] = cli_env
    elif "ENV" not in os.environ:
        os.environ["ENV"] = "d11"

    cli_test_type = config.getoption("--test-type")
    if cli_test_type:
        os.environ["TEST_TYPE"] = cli_test_type
    elif "TEST_TYPE" not in os.environ:
        os.environ["TEST_TYPE"] = "comparison"

    if config.getoption("--apim-as-iib"):
        os.environ["APIM_AS_IIB"] = "true"

    # Register TEST_ID / SERVICE_CONTRACT values as markers so -m works
    try:
        seen = set()
        for row in load_testcases():
            for tag in _row_tags(row):
                sanitized = _sanitize_mark(tag)
                if sanitized and sanitized not in seen:
                    seen.add(sanitized)
                    config.addinivalue_line(
                        "markers", f"{sanitized}: auto-generated tag from testcases.csv"
                    )
    except Exception:
        # Don't let a missing/misconfigured TESTCASES_FILE break collection
        pass

# --------------------------------------------------------------------------
# Resolve URLs and test type
# --------------------------------------------------------------------------
def get_env():
    return os.environ["ENV"]

def get_test_type():
    return os.environ["TEST_TYPE"]

def _env_letter_prefix():
    match = re.match(r"[a-zA-Z]+", os.getenv("ENV", ""))
    return match.group() if match else ""

def get_apim_base_url():
    if os.getenv("APIM_AS_IIB", "false").lower() == "true":
        return get_iib_base_url()
    return os.getenv("APIM_BASE_URL").replace("{environment}", _env_letter_prefix())

def get_iib_base_url():
    return os.getenv("IIB_BASE_URL").replace("{environment}", os.getenv("ENV"))


# --------------------------------------------------------------------------
# CSV loading + parametrization
# --------------------------------------------------------------------------

_TESTCASES_CACHE = None

def load_testcases():
    """Load and parse TESTCASES_FILE, caching the result for the process."""
    global _TESTCASES_CACHE
    if _TESTCASES_CACHE is None:
        csv_path = Path(os.getenv("TESTCASES_FILE"))
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            _TESTCASES_CACHE = list(csv.DictReader(f))
    return _TESTCASES_CACHE


def _sanitize_mark(name: str):
    """Turn a CSV value into a valid pytest mark / Python identifier."""
    name = (name or "").strip()
    if not name:
        return None
    name = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if name[0].isdigit():
        name = f"_{name}"
    return name


def pytest_generate_tests(metafunc):
    if "testcase_row" in metafunc.fixturenames:
        contracts = load_testcases()
        params = []
        ids = []
        for row in contracts:
            test_id = (row.get("TEST_ID") or "").strip()

            marks = []
            for tag in _row_tags(row):
                sanitized = _sanitize_mark(tag)
                if sanitized:
                    marks.append(getattr(pytest.mark, sanitized))

            params.append(pytest.param(row, marks=marks))
            ids.append(test_id)

        metafunc.parametrize("testcase_row", params, ids=ids, indirect=True)


@pytest.fixture
def testcase_row(request):
    row = request.param

    status = (row.get("STATUS") or "").strip().lower()
    if status == "disabled":
        test_id = (row.get("TEST_ID") or "").strip()
        pytest.skip(f"Test case '{test_id}' is disabled in testcases.csv file hence skipping.")

    row = resolve_row_tokens(row)

    return row


def pytest_bdd_before_scenario(request, feature, scenario):
    """
    Sets the Allure dynamic title. Must live in a pytest-bdd hook, not in the
    testcase_row fixture — allure-pytest-bdd creates its test_result container
    in its own pytest_bdd_before_scenario hook, which fires *after* fixture
    setup. Setting allure.dynamic.title() during fixture setup runs too early
    and hits a None container.
    """
    try:
        row = request.getfixturevalue("testcase_row")
    except Exception:
        # testcase_row wasn't resolved (e.g. test was skipped) — nothing to title
        return

    test_id = (row.get("TEST_ID") or "").strip()
    service_contract = (row.get("SERVICE_CONTRACT") or "").strip()
    condition = (row.get("CONDITION") or "").strip()

    title_parts = [p for p in (test_id, service_contract, condition) if p]
    if title_parts:
        allure.dynamic.title(" - ".join(title_parts))

# --------------------------------------------------------------------------
# Metadata loading — keyed by SC_ID for O(1) lookup
# --------------------------------------------------------------------------
def load_metadata():
    csv_path = Path(os.getenv("METADATA_FILE"))
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return {row["SERVICE_CONTRACT"]: row for row in reader}

METADATA = load_metadata()

@pytest.fixture
def metadata():
    return METADATA


# --------------------------------------------------------------------------
# Playwright request context
# --------------------------------------------------------------------------
@pytest.fixture
def request_context(playwright):
    rc = playwright.request.new_context(ignore_https_errors=True)
    yield rc
    rc.dispose()


# --------------------------------------------------------------------------
# API context container: holds APIM (always) and IIB (only for comparison)
# --------------------------------------------------------------------------
class DualAPIContext:
    """Bundles the APIM context and, when applicable, the IIB context."""
    def __init__(self, apim, iib=None):
        self.apim = apim
        self.iib = iib

    @property
    def is_comparison(self):
        return self.iib is not None


@pytest.fixture
def api_context(request_context):
    apim_ctx = APIContext(request_context)

    test_type = get_test_type()

    if test_type.lower() == "comparison":
        iib_ctx = APIContext(request_context)
        return DualAPIContext(apim=apim_ctx, iib=iib_ctx)

    # integration, sanity, etc. → APIM only
    return DualAPIContext(apim=apim_ctx, iib=None)


@pytest.fixture
def payload_factory():
    def _factory(payload_value: str, payload_placeholder_values: str, case_sensitive: bool = True):

        if not payload_value:
            return None  # no payload for this test case (e.g. GET request)

        raw_values = parse_validate_data(payload_placeholder_values)

        if _is_inline_payload(payload_value):
            return resolve_payload(payload_value, raw_values, case_sensitive=case_sensitive)
        else:
            template_path = Path(payload_value)
            return resolve_payload(template_path, raw_values, case_sensitive=case_sensitive)

    return _factory