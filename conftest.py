"""
This file contains custom pytest fixtures and configuration functions
"""

import html
import logging
import os
import platform
import uuid
from datetime import datetime
from functools import partial
from pathlib import Path
from zoneinfo import ZoneInfo

import allure_pytest_bdd.pytest_bdd_listener as bdd_listener
import pytest
from dotenv import load_dotenv

import utils.oracledb.swiftt.queries.swiftt_db_queries as swiftt_queries
from default_config import ALLURE_RESULTS_DIR, BULK_DATA_TEST, ENVIRONMENT, EXPORT_DB_ONLY, EXTERNAL_DB, \
    DEL_ALLURE_RESULTS_AUTO
from utils.bdd_utils.bdd_common_data import AllureReportConfiguration
from utils.mssql.SqlConnector import SqlConnector
from utils.oracledb.swiftt.swiftt_db_sql import get_from_swiftt, get_swiftt_connection_string
from utils.sqlite.db_operation_workflow import DB_PATH as CSV_DB_PATH
from utils.sqlite.db_operation_workflow import backup_db, copy_db_for_worker, export_db_to_csvs, generate_db_from_csvs

DB_PATH = Path(__file__).parent / "Service_contract_data.db"
DB_BACKUP_DIR = Path(__file__).parent / "local_db_backup"

allure_report_conf = AllureReportConfiguration(ALLURE_RESULTS_DIR)
ALLURE_RESULTS_PATH = Path(__file__).parent / ALLURE_RESULTS_DIR
_bulk_data_cache: list | None = None


def _fetch_bulk_data() -> list:
    global _bulk_data_cache
    if _bulk_data_cache is None:
        try:
            selected_data = get_from_swiftt(get_swiftt_connection_string(), swiftt_queries.ALL_CLIENTS)
            _bulk_data_cache = [row[0] for row in selected_data]
        except Exception as err_msg:
            logging.info("Failed to get bulk data from SWIFTT DB: %s", err_msg)
            _bulk_data_cache = []
    return _bulk_data_cache


def _clean_allure_results(alluredir: Path) -> None:
    if not alluredir.exists():
        alluredir.mkdir(parents=True, exist_ok=True)
        return
    for entry in alluredir.iterdir():
        try:
            if entry.is_dir() and not entry.is_symlink():
                import shutil

                shutil.rmtree(entry)
            else:
                entry.unlink()
        except OSError:
            logging.info("Could not remove the stale Allure result: %s", entry)


def _write_allure_env(alluredir: str) -> None:
    env_path = Path(alluredir) / "environment.properties"
    env_path.parent.mkdir(parents=True, exist_ok=True)

    env: dict[str, str] = {
        "Project": "Test Automation - APIM",
        "Test_Environment": os.getenv("ENVIRONMENT", "local"),
        "Python": platform.python_version(),
        "Pytest": pytest.__version__,
        "Date": datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%d %H:%M:%S %Z"),
    }

    for key in ("BUILD_NUMBER", "JOB_NAME", "GIT_BRANCH", "BRANCH_NAME", "GIT_COMMIT"):
        val = os.getenv(key)
        if val:
            env[key] = val

    with open(env_path, "w", encoding="utf-8") as f:
        for k, v in env.items():
            f.write(f"{k}={v}\n")


def _set_allure_description_html(item, original_get_html, bdd_utils):
    explicit_html = original_get_html(item)
    if explicit_html:
        return explicit_html

    try:
        test_data = bdd_utils.get_test_data(item)
        description = bdd_utils.get_allure_description(item, test_data.feature, test_data.scenario)
    except Exception:
        description = None

    if not description:
        return None

    return html.escape(description, quote=False).replace("\n", "<br/>")


def _update_allure_bdd_description_html() -> None:
    try:
        import allure_pytest_bdd.utils as bdd_utils

        original_get_html = bdd_utils.get_allure_description_html

        bdd_listener.get_allure_description_html = partial(
            _set_allure_description_html, original_get_html=original_get_html, bdd_utils=bdd_utils
        )
    except Exception:
        pass


def pytest_configure(config):
    _update_allure_bdd_description_html()
    if ENVIRONMENT.lower().startswith("d"):
        load_dotenv(".env.dev")
    else:
        load_dotenv(".env.uat")

    is_worker = hasattr(config, "workerinput")
    if not is_worker and DEL_ALLURE_RESULTS_AUTO:
        _clean_allure_results(ALLURE_RESULTS_PATH)

    if not is_worker and not EXPORT_DB_ONLY:
        logging.info("DB Generation: generating Service_contract_data.db from CSVs ...")
        generate_db_from_csvs()

    if BULK_DATA_TEST or EXTERNAL_DB:
        with SqlConnector() as conn:
            auto_db_env_parameters = conn.get_environment_config(ENVIRONMENT)
        auto_db_env_parameters["environment"] = ENVIRONMENT
    else:
        auto_db_env_parameters = {
            "SWIFTT_TRACE_Number": os.environ.get("SWIFTT_TRACE_Number", "1"),
            "environment": ENVIRONMENT,
        }
    pytest.auto_db_env_parameters = auto_db_env_parameters

    # Configure the transaction id
    value = "Integration_Automation_Test"
    pytest.AUTO_TRANSACTION_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, value))  # fb43edd1-87f3-5c6e-9d0e-302f62e6c218
    logging.info("Transaction ID: %s", pytest.AUTO_TRANSACTION_ID)

    _write_allure_env(str(Path(__file__).parent / "allure-results"))


def pytest_sessionfinish(session):
    # Export DB  back to CSV files
    is_worker = hasattr(session.config, "workerinput")
    if is_worker:
        return

    if CSV_DB_PATH.exists():
        logging.info("DB Export: exporting Service_contract_data.db back to CSVs ...")
        export_db_to_csvs()


# allure-report output path setup
def pytest_cmdline_main(config):
    project_root_dir = os.path.dirname(os.path.abspath(__file__))
    report_dir = str(config.option.allure_report_dir)
    json_report_dir = str(config.option.json_report_file)
    config.option.allure_report_dir = os.path.join(project_root_dir, report_dir)
    config.option.json_report_file = os.path.join(project_root_dir, json_report_dir)


# bulk data test scenarios
def pytest_generate_tests(metafunc):
    if "batch_data" in metafunc.fixturenames:
        fetched_data = _fetch_bulk_data()
        if not fetched_data:
            pytest.skip("Please set `BULK_DATA_TEST = True` in `local_config.py` to run the Bulk Data Test.")
        metafunc.parametrize("batch_data", fetched_data)


@pytest.fixture(autouse=True, scope="session")
def _db_worker_copy(request, tmp_path_factory):
    # for multiple processes
    is_worker = hasattr(request.config, "workerinput")

    if is_worker:
        worker_id = request.config.workerinput["workerid"]
        tmp_path = tmp_path_factory.mktemp("db_worker")
        worker_db = copy_db_for_worker(worker_id, tmp_path)

        # update the db path for multiple processes
        import utils.sqlite.db_operation_workflow as workflow

        workflow.DB_PATH = worker_db
        global DB_PATH
        DB_PATH = worker_db
    yield


@pytest.fixture(autouse=True, scope="session")
def _backup_db_on_change():
    if not DB_PATH.exists():
        yield
        return

    db_file_time_before = os.path.getmtime(DB_PATH)
    yield
    db_file_time_after = os.path.getmtime(DB_PATH)

    if db_file_time_before != db_file_time_after:
        backup_db(DB_PATH)
        logging.info("DB Backup Info: %s was modified during tests", DB_PATH.name)
