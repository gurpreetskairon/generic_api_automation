from __future__ import annotations

import csv
import logging
import shutil
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = REPO_ROOT / "Service_contract_data.db"
CSV_DIR = REPO_ROOT / "service_contract_data"
BACKUP_DIR = REPO_ROOT / "local_db_backup"


#################### generate DB from CSV files ####################
def _discover_csv_files(csv_dir: Path) -> list[Path]:
    # get csv files
    return sorted(csv_dir.glob("*.csv"))


def _create_table_from_csv(cur: sqlite3.Cursor, csv_path: Path) -> tuple[str, int]:
    # create table from csv files
    table_name = csv_path.stem

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        # add logic to handle the exceptions in csv files
        try:
            headers = next(reader)
        except StopIteration:
            logging.warning(f"Skipping empty CSV: {csv_path.name}")
            return table_name, 0
        if not headers or not any(header.strip() for header in headers):
            logging.warning(f"Skipping CSV with blank header row: {csv_path.name}")
            return table_name, 0
        columns = [f"[{h.strip()}]" for h in headers]
        col_list = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))

        cur.execute(f"DROP TABLE IF EXISTS [{table_name}]")
        cur.execute(f"CREATE TABLE [{table_name}] ({col_list})")

        rows = list(reader)
        if rows:
            cur.executemany(f"INSERT INTO [{table_name}] VALUES ({placeholders})", rows)

    return table_name, len(rows)


def generate_db_from_csvs(csv_dir: Path = CSV_DIR, db_path: Path = DB_PATH) -> None:
    # generate the db file
    if not csv_dir.exists():
        logging.warning("CSV directory not found: %s — skipping DB generation", csv_dir)
        return

    csv_files = _discover_csv_files(csv_dir)
    if not csv_files:
        logging.warning("No CSV files in %s — skipping DB generation", csv_dir)
        return

    # remove existing DB
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    total_rows = 0
    for csv_path in csv_files:
        table_name, row_count = _create_table_from_csv(cur, csv_path)
        total_rows += row_count
        logging.info("  %-40s %5d rows  <-  %s", table_name, row_count, csv_path.name)

    conn.commit()
    conn.close()

    logging.info("DB generated: %s (%d tables, %d rows)", db_path.name, len(csv_files), total_rows)


# export csv files from db
def _get_tables(conn: sqlite3.Connection) -> list[str]:
    # get names from all tables
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [row[0] for row in cur.fetchall() if not row[0].startswith("sqlite_")]


def _get_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    # get column names
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info([{table}])")
    return [row[1] for row in cur.fetchall()]


def _get_rows(conn: sqlite3.Connection, table: str) -> list[dict[str, object]]:
    # get rows value
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM [{table}]")
    columns = [desc[0] for desc in cur.description]
    return [dict(zip(columns, row)) for row in cur.fetchall()]


def export_db_to_csvs(db_path: Path = DB_PATH, csv_dir: Path = CSV_DIR) -> None:
    # export to csv files
    if not db_path.exists():
        logging.warning("DB not found: %s — skipping CSV export", db_path)
        return

    csv_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    tables = _get_tables(conn)

    total_rows = 0
    for table in tables:
        columns = _get_columns(conn, table)
        rows = _get_rows(conn, table)

        csv_path = csv_dir / f"{table}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

        total_rows += len(rows)
        logging.info("  %-40s %5d rows  ->  %s", table, len(rows), csv_path.name)

    conn.close()

    logging.info("CSVs exported: %d tables, %d rows -> %s", len(tables), total_rows, csv_dir)


# for multiple processes
def copy_db_for_worker(worker_id: str, tmp_path: Path) -> Path:
    """Copy the master DB to a worker-specific temp directory.

    Args:
        worker_id: xdist worker identifier (e.g. "gw0", "gw1").
        tmp_path:  Worker-local temporary directory.

    Returns:
        Path to the worker's private DB copy.
    """
    worker_db = tmp_path / f"Service_contract_data_{worker_id}.db"
    shutil.copy2(DB_PATH, worker_db)
    logging.info("Worker %s: DB copied to %s", worker_id, worker_db)
    return worker_db


# for DB backup
def backup_db(db_path: Path = DB_PATH) -> Path | None:
    """Create a timestamped backup of the DB if it exists.

    Returns:
        Path of the backup file, or None if DB didn't exist.
    """
    if not db_path.exists():
        return None

    from datetime import datetime

    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"service_contract_data_{timestamp}.db"
    shutil.copy2(db_path, backup_path)
    logging.info("DB backup: %s", backup_path)
    return backup_path
