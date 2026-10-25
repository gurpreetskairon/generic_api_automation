# APIM Migration Test Automation

This project is a pytest + pytest-bdd based API validation framework for comparing APIM responses against an existing IIB baseline or validating expected payload behavior from a CSV-driven test matrix.

The framework is designed around a simple idea:

- keep test data in CSV files instead of hardcoding one test per script
- drive reusable API scenarios from a single feature file
- resolve dynamic values in payloads and headers from tokens
- compare JSON/XML responses for diffs and report the outcome through Allure
- support both single-environment validation and APIM-vs-IIB comparison runs

The repository contains:

- `tests/` for pytest configuration, BDD step definitions, and CSV-driven test data
- `utils/` for reusable API, payload, comparison, and token helper logic
- `payloads/` for request payload XML/JSON templates
- `metadata/` for service-contract metadata such as path and endpoint mapping
- `merge_testdata.py` to merge scattered payload folders into a single `testcases.csv`
- `results/allure-report/` for generated Allure reports

---

## Project structure

```text
.
├── .env                              # environment and path settings
├── merge_testdata.py                 # merges folder-level testdata into one CSV
├── pytest.ini                       # pytest options and Allure output dir
├── requirements.txt                  # Python dependencies
├── metadata/
│   └── metadata.csv                  # service contract metadata
├── payloads/                        # request payload templates by batch/service contract
├── tests/
│   ├── conftest.py                  # pytest hooks, env overrides, fixture setup
│   ├── data/
│   │   └── testcases.csv            # master test matrix
│   ├── features/
│   │   └── generic_api.feature      # reusable BDD scenario
│   └── steps/
│       └── test_generic_api_steps.py
├── utils/
│   ├── api/
│   ├── comparison/
│   └── helpers/
├── results/
│   └── allure-report/
└── callbacks/
```

---

## Getting started

### Prerequisites

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Make sure the project has a valid `.env` file. It is used for defaults such as:

- `ENV`
- `TEST_TYPE`
- `APIM_BASE_URL`
- `IIB_BASE_URL`
- `TESTCASES_FILE`
- `METADATA_FILE`
- `PAYLOAD_DIR`
- `DATA_DIR`
- token-related keys such as `UUID_KEY`

Example `.env` values are already present in the repo and look like this:

```env
ENV=dev11
TEST_TYPE=comparison

IIB_BASE_URL=http://a2a{environment}.ssi.govt.nz/
APIM_BASE_URL=https://{environment}-apigw.int-npe.msd.govt.nz/

TESTCASES_FILE=./tests/data/testcases.csv
METADATA_FILE="./metadata/metadata.csv"
PAYLOAD_DIR=C:\NotBackedUp\APIM\payloads
DATA_DIR=C:\NotBackedUp\APIM\tests\data
```

---

## Running the tests

The project is pytest-based and uses the BDD scenario in `tests/features/generic_api.feature` for all rows in the CSV file.

### Basic run

```bash
pytest
```

This will run the generated parameterized tests based on the rows in `TESTCASES_FILE`.

### Override environment

```bash
pytest --env u10
```

This overrides the value in `.env` and sets `ENV` for the run.

### Override test type

```bash
pytest --test-type integration
```

This sets `TEST_TYPE` to a value used by the fixtures and enables the run style the project expects.

### Run APIM as IIB for a baseline/sanity scenario

```bash
pytest --apim-as-iib
```

This switches the APIM base URL generation so the request hits the IIB URL instead of the normal APIM base URL.

### Typical comparison run

```bash
pytest --env dev11 --test-type comparison
```

This is the most common setup for comparing APIM vs IIB output.

---

## Commandline options

There are two main CLI entry points in this project:

### 1) Merge CSV test data from payload folders

`merge_testdata.py` is a helper that finds `*_testcases.csv` files under a root folder, prepends a generated `TEST_ID` and service-contract/folder name, and writes a merged output file called `testcases.csv`.

Command:

```bash
python merge_testdata.py --input-dir <root_folder> --output-dir <output_folder>
```

Available options:

```bash
--input-dir             Root folder to search under
--output-dir            Folder where testcases.csv will be written
--test-id-col-name      Name of the generated ID column (default: TEST_ID)
--folder-col-name       Name of the folder/service-contract column (default: SERVICE_CONTRACT)
--testdata-name         Glob pattern to match testdata CSVs (default: *_testcases.csv)
--payload-col-name      Column containing payload values (default: PAYLOAD)
```

If `--input-dir` or `--output-dir` is omitted, the script falls back to `PAYLOAD_DIR` and `DATA_DIR` from `.env`.

Example:

```bash
python merge_testdata.py \
  --input-dir C:\NotBackedUp\APIM\payloads \
  --output-dir C:\NotBackedUp\APIM\tests\data \
  --test-id-col-name TEST_ID \
  --folder-col-name SERVICE_CONTRACT \
  --testdata-name "*_testcases.csv" \
  --payload-col-name PAYLOAD
```

This script also detects payload files in each folder that are not already referenced in the CSV and adds them automatically so the merged dataset remains complete.

### 2) Pytest runtime options

The framework adds extra pytest options in `tests/conftest.py`:

```bash
--env <name>           Override ENV from .env, example: --env u10
--test-type <type>     Override TEST_TYPE, example: --test-type integration
--apim-as-iib          Use the IIB base URL in place of the APIM base URL
```

Examples:

```bash
pytest --env dev11 --test-type comparison
pytest --env u10 --test-type integration --apim-as-iib
pytest --test-type sanity
```

---

## How CSV test data drives the suite

The project uses a CSV-based test matrix, with each row representing a single test scenario.

The master file is:

```text
tests/data/testcases.csv
```

A few key columns used by the framework are:

- `TEST_ID` - generated ID used for each row
- `SERVICE_CONTRACT` - matching key into `metadata.csv`
- `CONDITION` - human-readable scenario name
- `OVERRIDE_PATH` - overrides the endpoint path from metadata if needed
- `HEADER_PLACEHOLDER_VALUES` - values to replace in request headers
- `QUERY_STRING` - query string template
- `QUERY_STRING_PLACEHOLDER_VALUES` - placeholder values for query params
- `PAYLOAD` - payload file path or inline XML/JSON content
- `PAYLOAD_PLACEHOLDER_VALUES` - replacement values for the payload template
- `RESPONSE_CODE` - expected HTTP status code
- `VALIDATE_DATA` - JSON field validations to assert against the response
- `COMPARISON_TO_IGNORE` - fields that should be ignored in compare mode
- `STATUS` - set to `disabled` to skip execution for that row

Example row:

```csv
TC_1,SC575,Compare SC575 successful Match response,,"{""{short_env}"":""<get_short_env()>""}",,,,,,C:\NotBackedUp\APIM\payloads\Batch-1\SC575\SC575_default_payload.xml,"{
    ""{audit_id}"": ""<generate_uuid()>"",
    ""{correlation_id}"": ""<audit_id>"",
    ""{transaction_id}"": ""<audit_id>"",
    ""{request_date_time}"":""<resolve_date_token()>"",
    ""{ird_number}"": ""123344677"",
    ""{formatted_name}"": ""Allen, Gary"",
    ""{date_of_birth}"": ""1985-03-16"",
    ""{formatted_address}"": ""66 frye crescent Wanaka 9305"",
    ""{user_id}"": ""tbau0005""
}",,,200,,,,
```

The CSV row is consumed by the `testcase_row` fixture in `tests/conftest.py`, then the BDD step definitions in `tests/steps/test_generic_api_steps.py` build the request and validate the response.

---

## Metadata-driven endpoint mapping

The service contract metadata is defined in:

```text
metadata/metadata.csv
```

It contains columns such as:

- `SERVICE_CONTRACT`
- `PATH`
- `HEADER`
- `HTTP_METHOD`
- `BATCH`
- `OVERRIDE_APIM_BASE_URL`
- `OVERRIDE_IIB_BASE_URL`

This makes it easy to map a contract ID to the correct endpoint and request settings without repeating logic in the test case file.

Example:

```csv
SERVICE_CONTRACT,PATH,HEADER,HTTP_METHOD,BATCH
SC575,nz/govt/msd/integration/derived/participant/service/inquireparticipant/v1,HEADER_D,POST,Batch-1
```

The step file reads the contract row and constructs the endpoint, method, and headers before sending the request.

---

## Feature set and supported behavior

### 1) CSV-driven BDD execution

The scenario in `tests/features/generic_api.feature` is generic and reusable:

```gherkin
Feature: Generic API request validation

  Scenario: Validate an API response against expected data
    Given I fetch the endpoint
    And the request information
    When I send the request
    Then I should receive the expected status code
    And I validate the response data
```

This means you do not need to create a new feature for each endpoint. You add or update rows in the CSV and the same scenario executes them.

### 2) Tokenized dynamic values

The `utils/helpers/dynamic_tokens.py` helper supports tokens like these inside CSV values:

```text
<generate_uuid()>
<resolve_date_token()>
<random_int(1000,9999)>
<get_short_env()>
```

These values are resolved before the request is sent, making it easy to populate unique IDs, timestamps, and environment-specific values.

Examples from the project:

```json
"{audit_id}": "<generate_uuid()>"
"{request_date_time}": "<resolve_date_token()>"
"{short_env}": "<get_short_env()>"
```

### 3) Payload template resolution

The payload resolver understands both inline payload content and file-based payload templates.

- If `PAYLOAD` is a path to an XML or JSON file, the project loads it.
- If `PAYLOAD` contains raw JSON/XML content, it is treated as inline payload text.
- Placeholder values are substituted and targeted XML/JSON keys can be replaced structurally.

This is handled by `utils/comparison/payload_resolver.py`.

Examples:

```text
PAYLOAD=C:\NotBackedUp\APIM\payloads\Batch-1\SC575\SC575_default_payload.xml
```

or inline:

```json
{"Request":{"Name":"{formatted_name}"}}
```

### 4) Query-string and header substitution

The framework allows variables to be injected into headers and query strings before the request is sent.

Examples:

```csv
HEADER_PLACEHOLDER_VALUES,"{""{short_env}"":""<get_short_env()>""}"
QUERY_STRING_PLACEHOLDER_VALUES,"{""{clientNumber}"":""12345""}"
```

This turns request templates into fully concrete API calls.

### 5) APIM vs IIB comparison mode

When `TEST_TYPE=comparison`, the framework creates an `APIContext` for both APIM and IIB and sends both requests. It then compares the final payloads and reports differences.

This logic is written in:

- `tests/conftest.py`
- `utils/comparison/response_comparator.py`
- `utils/comparison/allure_reporting.py`

It supports:

- JSON/XML comparison
- field-level ignore rules via `COMPARISON_TO_IGNORE`
- schema/value diff classification
- side-by-side HTML comparison output and Allure attachments

Example:

```bash
pytest --env dev11 --test-type comparison
```

### 6) Validation against expected responses

When not in comparison mode, the framework validates the response using the fields in `VALIDATE_DATA`.

Example:

```csv
VALIDATE_DATA,"{""status"":""success"",""message"":""OK""}"
```

The project resolves the correct field using JSON or XML query patterns and compares the actual result to the expected value.

---

## Examples of common commands

### Build a merged CSV from payload folders

```bash
python merge_testdata.py --input-dir C:\NotBackedUp\APIM\payloads --output-dir C:\NotBackedUp\APIM\tests\data
```

### Run a single environment validation

```bash
pytest --env dev11 --test-type integration
```

### Run APIM vs IIB comparison

```bash
pytest --env dev11 --test-type comparison
```

### Force APIM to use IIB for baseline testing

```bash
pytest --env dev11 --test-type comparison --apim-as-iib
```

### Run with varying test selection using pytest marks

Because the framework auto-registers `TEST_ID` and `SERVICE_CONTRACT` values as pytest markers, you can filter by a contract or test case with commands like:

```bash
pytest -m SC575
pytest -m TC_1
```

---

## What the utils library is for

The `utils` package provides reusable infrastructure for the test suite.

### `utils/api/`

This folder contains API-layer utilities.

- `api_context.py` wraps Playwright request handling into a simple `APIContext` class
- `json_parser.py` helps extract values from JSON payloads using flexible query patterns
- `xml_parser.py` helps navigate and query XML payloads and response data

This is the layer that makes request construction and response lookup reusable across test cases.

### `utils/comparison/`

This folder contains the comparison logic.

- `payload_resolver.py` handles template substitution and structural replacement for JSON/XML payloads
- `response_comparator.py` compares two API responses and reports schema/value differences
- `allure_reporting.py` classifies mismatches and produces human-friendly Allure artifacts

This is the comparison engine used when validating APIM vs IIB output.

### `utils/helpers/`

This folder contains reusable helper functions and token plug-ins.

- `dynamic_tokens.py` registers functions and variables that can be referenced from CSV cells
- `helper.py` registers built-in token functions such as `generate_uuid` and `get_short_env`
- `date_util.py` contains date-related logic and supported token helpers

This is the place to add new dynamic token functions without changing the test framework itself.

---

## Notes and good practices

- Keep `TESTCASES_FILE` and `METADATA_FILE` in sync with the real data location in `.env`.
- Use `STATUS=disabled` in the CSV to skip a row without deleting it.
- Prefer parameterized, data-driven tests rather than adding one-off custom feature files.
- Store reusable payloads under `payloads/` and keep service metadata centralized in `metadata/metadata.csv`.
- Use the comparison ignore list (`COMPARISON_TO_IGNORE`) for known volatile fields like timestamps or correlation IDs.
- After each run, inspect the generated Allure report in `results/allure-report` for detailed diff information.

---

## Common workflow

A typical execution flow looks like this:

1. Prepare or update payload files under `payloads/`
2. Generate or refresh the merged CSV using `merge_testdata.py`
3. Update `metadata.csv` if paths or request metadata changed
4. Run the suite with pytest and the desired environment flags
5. Review the Allure report and inspect mismatches if any

This keeps the test suite data-driven, easy to extend, and consistent across multiple service contracts.

---

## Summary

This repository is built for automated API validation using:

- CSV-driven scenario execution
- reusable pytest-bdd steps
- dynamic token substitution
- payload template handling for JSON/XML
- APIM/IIB comparison workflows
- rich reporting in Allure

If you add new contracts, payload files, or token functions, the project is designed so that you mostly update data and templates rather than writing repetitive test code.
