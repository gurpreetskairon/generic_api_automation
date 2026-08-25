#!/usr/bin/env python3
"""
merge_testdata.py

Traverse all folders under a given input directory, look for files
matching a pattern (default '*_testcases.csv', e.g. 'SC43556_testcases.csv',
'DP334V2_testcases.csv') in each folder, prepend a sequential TEST_ID and
the folder's name as the first two columns, and append the combined
rows into a single output file called 'testcases.csv'.

Usage:
    python merge_testdata.py --input-dir <root_folder> --output-dir <output_folder>

    If --input-dir is omitted, it falls back to the PAYLOAD_DIR value from
    a .env file. If --output-dir is omitted, it falls back to the DATA_DIR
    value from a .env file.

Options:
    --input-dir       Root folder to search under
                       (falls back to PAYLOAD_DIR in .env if omitted)
    --output-dir      Folder where testcases.csv will be written
                       (falls back to DATA_DIR in .env if omitted)
    --test-id-col-name Name of the new sequential ID column (default: "TEST_ID")
    --folder-col-name Name of the new folder-name column (default: "SERVICE_CONTRACT")
    --testdata-name   Glob pattern of the testdata file(s) to look for
                       (default: "*_testcases.csv")
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
    env_path = env_path or Path(".env")

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


def merge_testdata_files(
    input_dir: Path,
    output_file: Path,
    test_id_col_name: str,
    folder_col_name: str,
    testdata_pattern: str,
    payload_col_name: str = "PAYLOAD",
):
    matches = find_testdata_files(input_dir, testdata_pattern)

    if not matches:
        print(f"No files matching '{testdata_pattern}' found under '{input_dir}'.")
        return 0

    # Delete any existing output file before starting
    if output_file.exists():
        output_file.unlink()
        print(f"Deleted existing file: {output_file}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    header_written = False
    files_processed = 0
    rows_written = 0
    test_id_counter = 1  # sequential across the entire output file

    with open(output_file, "w", newline="", encoding="utf-8-sig") as out_f:
        writer = None

        for folder_path, testdata_path in matches:
            folder_name = folder_path.name

            try:
                rows = read_csv_rows(testdata_path)
            except Exception as e:
                print(f"  Skipping '{testdata_path}': could not read file ({e})")
                continue

            if not rows:
                print(f"  Skipping '{testdata_path}': file is empty")
                continue

            header = rows[0]
            data_rows = rows[1:]

            # Find the Payload column so we can prefix it with the folder path
            payload_idx = None
            if payload_col_name in header:
                payload_idx = header.index(payload_col_name)
            else:
                print(f"  Warning: '{payload_col_name}' column not found in '{testdata_path}', "
                      f"leaving payload values unchanged")

            if writer is None:
                writer = csv.writer(out_f)

            if not header_written:
                # First file: write header (with TEST_ID and folder columns prepended)
                writer.writerow([test_id_col_name, folder_col_name] + header)
                header_written = True

            # Track which payload file names are already referenced in this
            # testdata file, so we can detect .xml/.json files present in the
            # folder but missing from the Payload column.
            referenced_payloads = set()

            for row in data_rows:
                if payload_idx is not None and payload_idx < len(row) and row[payload_idx]:
                    payload_value = row[payload_idx].strip()
                    row = list(row)
                    if Path(payload_value).suffix.lower() in (".xml", ".json"):
                        # Looks like a payload file name -> prefix with folder path
                        referenced_payloads.add(payload_value)
                        row[payload_idx] = str(folder_path / payload_value)
                    else:
                        # Not a file reference (e.g. inline JSON/XML payload) -> leave as-is
                        row[payload_idx] = payload_value
                writer.writerow([f"TC_{test_id_counter}", folder_name] + row)
                test_id_counter += 1
                rows_written += 1

            # Check the folder for .xml/.json payload files not already referenced
            if payload_idx is not None:
                num_cols = len(header)
                found_payload_files = sorted(
                    p.name for p in folder_path.iterdir()
                    if p.is_file() and p.suffix.lower() in (".xml", ".json")
                )
                missing_payload_files = [
                    name for name in found_payload_files if name not in referenced_payloads
                ]

                for missing_name in missing_payload_files:
                    extra_row = [""] * num_cols
                    extra_row[payload_idx] = str(folder_path / missing_name)
                    writer.writerow([f"TC_{test_id_counter}", folder_name] + extra_row)
                    test_id_counter += 1
                    rows_written += 1
                    print(f"  Added missing payload file '{missing_name}' from folder '{folder_name}'")

            files_processed += 1
            print(f"  Merged '{testdata_path}' ({len(data_rows)} rows) from folder '{folder_name}'")

    print(
        f"\nDone. Processed {files_processed} testdata file(s), "
        f"wrote {rows_written} data row(s) to '{output_file}'."
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
    args = parser.parse_args()

    # Load .env (without overwriting anything already set in the real
    # environment), then fall back to it for any dir not given on the CLI.
    load_env_file()

    input_dir_value = args.input_dir or os.environ.get("PAYLOAD_DIR")
    output_dir_value = args.output_dir or os.environ.get("DATA_DIR")

    if not input_dir_value:
        print("Error: --input-dir was not provided and PAYLOAD_DIR is not set in .env.")
        sys.exit(1)
    if not output_dir_value:
        print("Error: --output-dir was not provided and DATA_DIR is not set in .env.")
        sys.exit(1)

    input_dir = Path(input_dir_value).expanduser().resolve()
    output_dir = Path(output_dir_value).expanduser().resolve()

    if not input_dir.is_dir():
        print(f"Error: input directory '{input_dir}' does not exist or is not a directory.")
        sys.exit(1)

    output_file = output_dir / "testcases.csv"

    merge_testdata_files(
        input_dir=input_dir,
        output_file=output_file,
        test_id_col_name=args.test_id_col_name,
        folder_col_name=args.folder_col_name,
        testdata_pattern=args.testdata_name,
        payload_col_name=args.payload_col_name,
    )


if __name__ == "__main__":
    main()