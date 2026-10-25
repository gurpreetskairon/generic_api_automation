#!/usr/bin/env python3
"""
merge_testdata.py

Traverse all folders under a given input directory, look for files
matching a pattern (default '*_testcases.csv', e.g. 'SC43556_testcases.csv',
'DP334V2_testcases.csv') in each folder, prepend a sequential TEST_ID and
the folder's name as the first two columns, insert a merged TAGS column
right after that, and append the combined rows into a single output file
called 'testcases.csv'.

The TAGS column is built by:
  - Taking the TAGS value from the source *_testcases.csv row, if that
    column exists there (comma-separated values are left as-is).
  - Appending the BATCH number for that row's SERVICE_CONTRACT, looked up
    from metadata.csv (comma-separated with any existing tags).
  - If there is no existing TAGS value (column missing or empty), the
    output TAGS cell is just the BATCH number on its own (no leading comma).
  - If no BATCH value is found either, whatever existing tags there are
    (or an empty string) are used as-is.

metadata.csv is loaded once into an in-memory dict keyed by SERVICE_CONTRACT
(unique) -> BATCH, so it isn't re-read for every row.

Rows in a source *_testcases.csv file that are completely empty (every
column blank/whitespace-only) are skipped and not written to the merged
output file.

Usage:
    python merge_testdata.py --input-dir <root_folder> --output-dir <output_folder> --metadata-file <path_to_metadata.csv>

    If --input-dir is omitted, it falls back to the PAYLOAD_DIR value from
    a .env file. If --output-dir is omitted, it falls back to the DATA_DIR
    value from a .env file. If --metadata-file is omitted, it falls back to
    the METADATA_FILE value from a .env file.

Options:
    --input-dir        Root folder to search under
                        (falls back to PAYLOAD_DIR in .env if omitted)
    --output-dir        Folder where testcases.csv will be written
                        (falls back to DATA_DIR in .env if omitted)
    --metadata-file     Path to metadata.csv, used to look up BATCH numbers
                        by SERVICE_CONTRACT
                        (falls back to METADATA_FILE in .env if omitted)
    --test-id-col-name  Name of the new sequential ID column (default: "TEST_ID")
    --folder-col-name   Name of the new folder-name column (default: "SERVICE_CONTRACT")
    --testdata-name     Glob pattern of the testdata file(s) to look for
                        (default: "*_testcases.csv")
    --payload-col-name  Name of the payload column in the testdata files (default: "PAYLOAD")
    --tags-col-name     Name of the tags column, in both the source testdata
                        files (if present) and the merged output (default: "TAGS")
    --batch-col-name    Name of the batch column in metadata.csv (default: "BATCH")
    --include-missing-payloads
                        If set, also add a test row for any .xml/.json file
                        found in a folder that isn't referenced by any row
                        in that folder's *_testcases.csv file(s). Off by
                        default.
"""

import argparse
import csv
import fnmatch
import os
import sys
from pathlib import Path


def load_env_file(env_path: Path = None):
    """
    Load key=value pairs from a .env file into os.environ, without
    overwriting any variable that is already set in the environment.

    Uses python-dotenv if it's installed; otherwise falls back to a small
    built-in parser so this script has no hard dependency on it.
    """
    env_path = env_path or Path("../.env")

    try:
        from dotenv import dotenv_values  # type: ignore

        if env_path.is_file():
            for key, value in dotenv_values(env_path).items():
                if key and value is not None and key not in os.environ:
                    os.environ[key] = value
        return
    except ImportError:
        pass

    # Minimal fallback .env parser: KEY=VALUE per line, '#' comments,
    # optional surrounding quotes stripped.
    if not env_path.is_file():
        return

    try:
        with open(env_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError as e:
        print(f"Warning: could not read .env file '{env_path}': {e}")


def find_testdata_files(root_dir: Path, testdata_pattern: str):
    """
    Walk all folders under root_dir and yield (folder_path, testdata_file_path)
    for every file in every folder whose name matches testdata_pattern
    (a glob-style pattern, e.g. '*_testcases.csv'). A folder may contain
    more than one matching file (e.g. 'SC43556_testcases.csv' and
    'DP334V2_testcases.csv' in the same folder); each match is yielded
    separately.

    Results are sorted by (folder_path, file_name) so the output is
    deterministic/reproducible.
    """
    matches = []
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if fnmatch.fnmatch(filename, testdata_pattern):
                folder_path = Path(dirpath)
                testdata_path = folder_path / filename
                matches.append((folder_path, testdata_path))

    matches.sort(key=lambda item: (str(item[0]), item[1].name))
    return matches


def read_csv_rows(path: Path):
    """
    Read a CSV file's rows, trying a few common encodings in order.
    Windows-exported CSVs are often cp1252 rather than utf-8 (e.g. smart
    quotes, en-dashes, non-breaking spaces), so we fall back gracefully.
    latin-1 is tried last since it never raises a decode error.
    """
    encodings_to_try = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
    last_error = None

    for encoding in encodings_to_try:
        try:
            with open(path, "r", newline="", encoding=encoding) as f:
                rows = list(csv.reader(f))
            if encoding != "utf-8-sig" and encoding != "utf-8":
                print(f"  Note: '{path}' was not UTF-8; read successfully using '{encoding}'")
            return rows
        except UnicodeDecodeError as e:
            last_error = e
            continue

    # Should not normally reach here since latin-1 never fails, but just in case
    raise last_error


def load_metadata_lookup(
    metadata_path: Path,
    service_contract_col: str = "SERVICE_CONTRACT",
    batch_col: str = "BATCH",
):
    """
    Load the metadata file into a dict keyed by SERVICE_CONTRACT (unique) ->
    BATCH, so BATCH numbers can be looked up in O(1) per row instead of
    re-scanning the metadata file for every test case.

    Returns an empty dict (with a warning) if the file is missing, empty, or
    doesn't have the expected columns, so a missing/misconfigured metadata
    file degrades to "no BATCH tags added" rather than crashing the merge.
    """
    if not metadata_path.is_file():
        print(f"Warning: metadata file '{metadata_path}' not found; "
              f"BATCH tags will be left blank.")
        return {}

    try:
        rows = read_csv_rows(metadata_path)
    except Exception as e:
        print(f"Warning: could not read metadata file '{metadata_path}' ({e}); "
              f"BATCH tags will be left blank.")
        return {}

    if not rows:
        print(f"Warning: metadata file '{metadata_path}' is empty; "
              f"BATCH tags will be left blank.")
        return {}

    header = rows[0]
    if service_contract_col not in header or batch_col not in header:
        print(f"Warning: metadata file '{metadata_path}' is missing "
              f"'{service_contract_col}' or '{batch_col}' column; "
              f"BATCH tags will be left blank.")
        return {}

    sc_idx = header.index(service_contract_col)
    batch_idx = header.index(batch_col)

    lookup = {}
    for row in rows[1:]:
        if sc_idx < len(row) and row[sc_idx].strip():
            service_contract = row[sc_idx].strip()
            batch_value = row[batch_idx].strip() if batch_idx < len(row) else ""
            lookup[service_contract] = batch_value

    print(f"Loaded {len(lookup)} SERVICE_CONTRACT -> BATCH entries from '{metadata_path}'.")
    return lookup


# Canonical column order for the merged output file, everything after
# TEST_ID / SERVICE_CONTRACT / TAGS. This is fixed regardless of what order
# (or subset) of columns a given source *_testcases.csv file happens to use,
# so mismatched column ordering across folders can never shift data into the
# wrong column.
OUTPUT_COLUMNS = [
    "CONDITION",
    "OVERRIDE_CONTRACT_TYPE",
    "OVERRIDE_PATH",
    "HEADER_PLACEHOLDER_VALUES",
    "OVERRIDE_HTTP_METHOD",
    "QUERY_STRING",
    "QUERY_STRING_PLACEHOLDER_VALUES",
    "OVERRIDE_QUERY_STRING_FOR_IIB",
    "OVERRIDE_QUERY_STRING_PLACEHOLDER_VALUES_FOR_IIB",
    "PAYLOAD",
    "PAYLOAD_PLACEHOLDER_VALUES",
    "OVERRIDE_PAYLOAD_FOR_IIB",
    "OVERRIDE_PAYLOAD_PLACEHOLDER_VALUES_FOR_IIB",
    "COMPARISON_TO_IGNORE",
    "RESPONSE_CODE",
    "VALIDATE_DATA",
    "ASYNC_COMPARISON_TO_IGNORE",
    "ASYNC_RESPONSE_CODE",
    "ASYNC_VALIDATE_DATA",
    "STATUS",
]


def read_csv_dict_rows(path: Path):
    """
    Read a CSV file as a list of dicts keyed by its own header/column names,
    trying a few common encodings in order (see read_csv_rows for rationale).

    Returns (fieldnames, rows). Reading by column name (rather than by
    position) is what lets the caller safely combine files whose columns
    are in a different order, or missing/extra columns, without misaligning
    data.
    """
    encodings_to_try = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
    last_error = None

    for encoding in encodings_to_try:
        try:
            with open(path, "r", newline="", encoding=encoding) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                fieldnames = list(reader.fieldnames or [])
            if encoding != "utf-8-sig" and encoding != "utf-8":
                print(f"  Note: '{path}' was not UTF-8; read successfully using '{encoding}'")
            return fieldnames, rows
        except UnicodeDecodeError as e:
            last_error = e
            continue

    # Should not normally reach here since latin-1 never fails, but just in case
    raise last_error


def is_empty_row(row: dict) -> bool:
    """
    A row is considered empty if every value in it is missing, None, or
    whitespace-only. DictReader can produce values of None (short rows) or
    a list (extra unnamed columns under the None key), so both are handled.
    """
    for value in row.values():
        if value is None:
            continue
        if isinstance(value, list):
            if any((v or "").strip() for v in value):
                return False
            continue
        if value.strip():
            return False
    return True


def merge_testdata_files(
    input_dir: Path,
    output_file: Path,
    test_id_col_name: str,
    folder_col_name: str,
    testdata_pattern: str,
    metadata_lookup: dict,
    payload_col_name: str = "PAYLOAD",
    tags_col_name: str = "TAGS",
    output_columns: list = None,
    include_missing_payloads: bool = False,
):
    output_columns = output_columns if output_columns is not None else OUTPUT_COLUMNS

    matches = find_testdata_files(input_dir, testdata_pattern)

    if not matches:
        print(f"No files matching '{testdata_pattern}' found under '{input_dir}'.")
        return 0

    # Delete any existing output file before starting
    if output_file.exists():
        output_file.unlink()
        print(f"Deleted existing file: {output_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    files_processed = 0
    rows_written = 0
    rows_skipped_empty = 0
    test_id_counter = 1  # sequential across the entire output file
    warned_missing_batch = set()  # avoid repeating the same warning per folder

    with open(output_file, "w", newline="", encoding="utf-8-sig") as out_f:
        writer = csv.writer(out_f)
        # The output column order is fixed up front, independent of any
        # source file's column order.
        writer.writerow([test_id_col_name, folder_col_name, tags_col_name] + output_columns)

        for folder_path, testdata_path in matches:
            folder_name = folder_path.name

            try:
                fieldnames, data_rows = read_csv_dict_rows(testdata_path)
            except Exception as e:
                print(f"  Skipping '{testdata_path}': could not read file ({e})")
                continue

            if not fieldnames:
                print(f"  Skipping '{testdata_path}': file is empty or has no header")
                continue

            # Flag columns present in the source file that don't map to any
            # known output column (typos, unexpected extras) — data in these
            # columns is dropped, so it's worth surfacing.
            known_cols = set(output_columns) | {tags_col_name}
            unexpected_cols = [c for c in fieldnames if c and c not in known_cols]
            if unexpected_cols:
                print(f"  Note: '{testdata_path}' has column(s) not in the expected schema "
                      f"and their data will be ignored: {', '.join(unexpected_cols)}")

            missing_cols = [c for c in output_columns if c not in fieldnames]
            if missing_cols:
                print(f"  Note: '{testdata_path}' is missing column(s) {', '.join(missing_cols)}; "
                      f"they will be left blank for its rows.")

            # BATCH number for this folder's SERVICE_CONTRACT, looked up once per file
            batch_value = metadata_lookup.get(folder_name, "")
            if not batch_value and folder_name not in warned_missing_batch:
                print(f"  Warning: no BATCH entry found in metadata for "
                      f"SERVICE_CONTRACT '{folder_name}'; TAGS will not include a batch number.")
                warned_missing_batch.add(folder_name)

            # Track which payload file names are already referenced in this
            # testdata file, so we can detect .xml/.json files present in the
            # folder but missing from the Payload column.
            referenced_payloads = set()

            file_rows_skipped = 0
            for row in data_rows:
                if is_empty_row(row):
                    file_rows_skipped += 1
                    rows_skipped_empty += 1
                    continue

                payload_value = (row.get(payload_col_name) or "").strip()
                if payload_value and Path(payload_value).suffix.lower() in (".xml", ".json"):
                    # Looks like a payload file name -> prefix with folder path
                    referenced_payloads.add(payload_value)
                    resolved_payload_value = str(folder_path / payload_value)
                else:
                    # Not a file reference (e.g. inline JSON/XML payload), or empty -> leave as-is
                    resolved_payload_value = payload_value

                orig_tags = (row.get(tags_col_name) or "").strip()
                if orig_tags and batch_value:
                    merged_tags = f"{orig_tags},{batch_value}"
                else:
                    merged_tags = orig_tags or batch_value  # whichever one is non-empty (or "")

                output_row = [f"TC_{test_id_counter}", folder_name, merged_tags]
                for col in output_columns:
                    if col == payload_col_name:
                        output_row.append(resolved_payload_value)
                    else:
                        output_row.append(row.get(col) or "")

                writer.writerow(output_row)
                test_id_counter += 1
                rows_written += 1

            if file_rows_skipped:
                print(f"  Skipped {file_rows_skipped} empty row(s) in '{testdata_path}'")

            # Check the folder for .xml/.json payload files not already referenced
            # (only when explicitly requested via include_missing_payloads)
            if include_missing_payloads and payload_col_name in output_columns:
                found_payload_files = sorted(
                    p.name for p in folder_path.iterdir()
                    if p.is_file() and p.suffix.lower() in (".xml", ".json")
                )
                missing_payload_files = [
                    name for name in found_payload_files if name not in referenced_payloads
                ]

                for missing_name in missing_payload_files:
                    output_row = [f"TC_{test_id_counter}", folder_name, batch_value]
                    for col in output_columns:
                        output_row.append(str(folder_path / missing_name) if col == payload_col_name else "")

                    writer.writerow(output_row)
                    test_id_counter += 1
                    rows_written += 1
                    print(f"  Added missing payload file '{missing_name}' from folder '{folder_name}'")

            files_processed += 1
            print(f"  Merged '{testdata_path}' ({len(data_rows)} rows) from folder '{folder_name}'")

    print(
        f"\nDone. Processed {files_processed} testdata file(s), "
        f"wrote {rows_written} data row(s) to '{output_file}'"
        + (f" (skipped {rows_skipped_empty} empty row(s))." if rows_skipped_empty else ".")
    )
    return files_processed


def main():
    parser = argparse.ArgumentParser(
        description="Merge *_testcases.csv files from all subfolders into a single testcases.csv"
    )
    parser.add_argument(
        "--input-dir",
        required=False,
        default=None,
        help="Root folder to search under (falls back to PAYLOAD_DIR in .env if omitted)",
    )
    parser.add_argument(
        "--output-dir",
        required=False,
        default=None,
        help="Folder where testcases.csv will be written (falls back to DATA_DIR in .env if omitted)",
    )
    parser.add_argument(
        "--metadata-file",
        required=False,
        default=None,
        help="Path to metadata.csv, used to look up BATCH numbers by "
             "SERVICE_CONTRACT (falls back to METADATA_FILE in .env if omitted)",
    )
    parser.add_argument(
        "--test-id-col-name",
        default="TEST_ID",
        help="Name of the new sequential ID column, values written as TC_1, TC_2, ... (default: TEST_ID)",
    )
    parser.add_argument(
        "--folder-col-name",
        default="SERVICE_CONTRACT",
        help="Name of the new column that holds the folder name (default: SERVICE_CONTRACT)",
    )
    parser.add_argument(
        "--testdata-name",
        default="*_testcases.csv",
        help="Glob pattern of the testdata file(s) to look for in each folder, "
             "e.g. 'SC43556_testcases.csv', 'DP334V2_testcases.csv' (default: *_testcases.csv)",
    )
    parser.add_argument(
        "--payload-col-name",
        default="PAYLOAD",
        help="Name of the column in the testdata file holding the payload file name (default: PAYLOAD)",
    )
    parser.add_argument(
        "--tags-col-name",
        default="TAGS",
        help="Name of the tags column, in both the source testdata files (if present) "
             "and the merged output file (default: TAGS)",
    )
    parser.add_argument(
        "--batch-col-name",
        default="BATCH",
        help="Name of the batch column in metadata.csv (default: BATCH)",
    )
    parser.add_argument(
        "--include-missing-payloads",
        action="store_true",
        default=False,
        help="Also add a test row for any .xml/.json file in a folder that "
             "isn't referenced by any row in that folder's *_testcases.csv "
             "file(s). Off by default.",
    )
    args = parser.parse_args()

    # Load .env (without overwriting anything already set in the real
    # environment), then fall back to it for any dir not given on the CLI.
    load_env_file()

    input_dir_value = args.input_dir or os.environ.get("PAYLOAD_DIR")
    output_dir_value = args.output_dir or os.environ.get("DATA_DIR")
    metadata_file_value = args.metadata_file or os.environ.get("METADATA_FILE")

    if not input_dir_value:
        print("Error: --input-dir was not provided and PAYLOAD_DIR is not set in .env.")
        sys.exit(1)
    if not output_dir_value:
        print("Error: --output-dir was not provided and DATA_DIR is not set in .env.")
        sys.exit(1)
    if not metadata_file_value:
        print("Error: --metadata-file was not provided and METADATA_FILE is not set in .env.")
        sys.exit(1)

    input_dir = Path(input_dir_value).expanduser().resolve()
    output_dir = Path(output_dir_value).expanduser().resolve()
    metadata_file = Path(metadata_file_value).expanduser().resolve()

    if not input_dir.is_dir():
        print(f"Error: input directory '{input_dir}' does not exist or is not a directory.")
        sys.exit(1)

    metadata_lookup = load_metadata_lookup(
        metadata_file,
        batch_col=args.batch_col_name,
    )

    output_file = output_dir / "testcases.csv"

    merge_testdata_files(
        input_dir=input_dir,
        output_file=output_file,
        test_id_col_name=args.test_id_col_name,
        folder_col_name=args.folder_col_name,
        testdata_pattern=args.testdata_name,
        metadata_lookup=metadata_lookup,
        payload_col_name=args.payload_col_name,
        tags_col_name=args.tags_col_name,
        include_missing_payloads=args.include_missing_payloads,
    )


if __name__ == "__main__":
    main()
