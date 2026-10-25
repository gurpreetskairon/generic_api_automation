import os
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "Service_contract_data.db"

# run: python scripts/db_setup_sc827.py
SC827_COLUMNS = [
    "condition",
    "user_id",
    "source_system",
    "date_of_birth",
    "gender",
    "address_line1",
    "address_line2",
    "suburb",
    "city",
    "post_code",
    "country_code",
    "country_of_birth",
    "residency_code",
    "residency_effective_date",
    "residency_description",
    "contact_period_start",
    "security_token_type",
    "ird_number",
    "marital_status",
    "marital_status_effective_date",
    "partner_client_number",
    "partner_relationship_start_date",
    "partner_from_type",
    "partner_to_type",
    "expected_result_code",
    "expected_message",
    "expected_subresult_code",
    "expected_subresult_message",
]


def connect_db():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    return sqlite3.connect(DB_PATH)


def add_sc827_endpoints(cur):
    """
    SC827 uses the same manageparticipant endpoint path as SC829.
    This copies SC829 AZURE/IIB endpoint rows to SC827 if missing.
    """

    cur.execute("""
        INSERT INTO ENDPOINTS (SERVICE_CONTRACT, SYSTEM, PATH)
        SELECT 'SC827', e.SYSTEM, e.PATH
        FROM ENDPOINTS e
        WHERE e.SERVICE_CONTRACT = 'SC829'
          AND NOT EXISTS (
              SELECT 1
              FROM ENDPOINTS existing
              WHERE existing.SERVICE_CONTRACT = 'SC827'
                AND existing.SYSTEM = e.SYSTEM
                AND existing.PATH = e.PATH
          )
    """)


def create_sc827_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS SC827 (
            condition TEXT PRIMARY KEY,
            user_id TEXT,
            source_system TEXT,
            date_of_birth TEXT,
            gender TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            suburb TEXT,
            city TEXT,
            post_code TEXT,
            country_code TEXT,
            country_of_birth TEXT,
            residency_code TEXT,
            residency_effective_date TEXT,
            residency_description TEXT,
            contact_period_start TEXT,
            security_token_type TEXT,
            ird_number TEXT,
            marital_status TEXT,
            marital_status_effective_date TEXT,
            partner_client_number TEXT,
            partner_relationship_start_date TEXT,
            partner_from_type TEXT,
            partner_to_type TEXT,
            expected_result_code TEXT,
            expected_message TEXT,
            expected_subresult_code TEXT,
            expected_subresult_message TEXT
        )
    """)


def ensure_sc827_columns(cur):
    """
    Adds new SC827 columns to an existing local SQLite table.

    CREATE TABLE IF NOT EXISTS does not update an already-created table,
    so ALTER TABLE is required when columns are added later.
    """

    cur.execute("PRAGMA table_info(SC827)")
    existing_columns = {row[1] for row in cur.fetchall()}

    required_columns = {
        "user_id": "TEXT",
        "source_system": "TEXT",
        "date_of_birth": "TEXT",
        "gender": "TEXT",
        "address_line1": "TEXT",
        "address_line2": "TEXT",
        "suburb": "TEXT",
        "city": "TEXT",
        "post_code": "TEXT",
        "country_code": "TEXT",
        "country_of_birth": "TEXT",
        "residency_code": "TEXT",
        "residency_effective_date": "TEXT",
        "residency_description": "TEXT",
        "contact_period_start": "TEXT",
        "security_token_type": "TEXT",
        "ird_number": "TEXT",
        "marital_status": "TEXT",
        "marital_status_effective_date": "TEXT",
        "partner_client_number": "TEXT",
        "partner_relationship_start_date": "TEXT",
        "partner_from_type": "TEXT",
        "partner_to_type": "TEXT",
        "expected_result_code": "TEXT",
        "expected_message": "TEXT",
        "expected_subresult_code": "TEXT",
        "expected_subresult_message": "TEXT",
    }

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            cur.execute(f"ALTER TABLE SC827 ADD COLUMN {column_name} {column_type}")
            print(f"Added SC827 column: {column_name}")


def create_sc827_partner_pool_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS SC827_PARTNER_POOL (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            environment TEXT NOT NULL DEFAULT 'dev11',
            partner_client_number TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL DEFAULT 'AVAILABLE',
            used_for_condition TEXT,
            reserved_transaction_id TEXT,
            created_client_number TEXT,
            reserved_at TEXT,
            used_at TEXT,
            notes TEXT
        )
    """)


def build_row(**overrides):
    """
    Base SC827 row with valid client details.

    Override only the fields needed for each scenario.
    """

    row = {
        "condition": None,
        "user_id": "tbau0005",
        "source_system": "SAL",
        "date_of_birth": "2000-01-01",
        "gender": "FEMALE",
        "address_line1": "56 The Terrace",
        "address_line2": "",
        "suburb": "",
        "city": "Wellington",
        "post_code": "",
        "country_code": "NZ",
        "country_of_birth": "NZ",
        "residency_code": "TVSA",
        "residency_effective_date": "2014-08-29",
        "residency_description": "Resident",
        "contact_period_start": "2017-03-15",
        "security_token_type": "USER",
        "ird_number": None,
        "marital_status": "MRRD",
        "marital_status_effective_date": "2014-08-29",
        "partner_client_number": None,
        "partner_relationship_start_date": None,
        "partner_from_type": "PARTNER",
        "partner_to_type": "PARTNER",
        "expected_result_code": None,
        "expected_message": None,
        "expected_subresult_code": None,
        "expected_subresult_message": None,
    }

    row.update(overrides)
    return row


def insert_sc827_rows(cur):
    rows = [
        build_row(
            condition="valid_register_client_without_partner",
            residency_code="NZCI",
            residency_effective_date=None,
            residency_description=None,
            contact_period_start=None,
            security_token_type="USER",
            ird_number=None,
            marital_status="SNGL",
            marital_status_effective_date=None,
            expected_result_code="82700",
            expected_message="Transaction Successful",
        ),
        build_row(
            condition="valid_register_client_with_partner",
            address_line2="Line2",
            suburb="Wellington",
            security_token_type="SYSTEM",
            ird_number="",
            partner_client_number=None,
            partner_relationship_start_date="2014-08-29",
            expected_result_code="82700",
            expected_message="Transaction Successful",
        ),
        build_row(
            condition="missing_mandatory_person_data",
            residency_code="NZCI",
            residency_effective_date=None,
            residency_description=None,
            contact_period_start=None,
            security_token_type="USER",
            ird_number=None,
            marital_status="SNGL",
            marital_status_effective_date=None,
            expected_result_code="82701",
            expected_message="Transaction Unsuccessful",
            expected_subresult_code="82710",
            expected_subresult_message="At least one mandatory field is missing",
        ),
        build_row(
            condition="invalid_ird_number_format",
            residency_code="NZCI",
            residency_effective_date=None,
            residency_description=None,
            contact_period_start=None,
            security_token_type="USER",
            ird_number="ABC123",
            marital_status="SNGL",
            marital_status_effective_date=None,
            expected_result_code="82701",
            expected_message="Transaction Unsuccessful",
            expected_subresult_code="82711",
            expected_subresult_message="IRD Number format error",
        ),
        build_row(
            condition="dob_after_system_date",
            residency_code="NZCI",
            residency_effective_date=None,
            residency_description=None,
            contact_period_start=None,
            security_token_type="USER",
            date_of_birth="2099-01-01",
            ird_number=None,
            marital_status="SNGL",
            marital_status_effective_date=None,
            expected_result_code="82701",
            expected_message="Transaction Unsuccessful",
            expected_subresult_code="82713",
            expected_subresult_message="DOB cannot be after system date",
        ),
        build_row(
            condition="partner_client_number_does_not_exist",
            address_line2="Line2",
            suburb="Wellington",
            security_token_type="SYSTEM",
            ird_number="",
            partner_client_number="333333333",
            partner_relationship_start_date="2014-08-29",
            partner_from_type="PARTNER",
            partner_to_type="PARTNER",
            residency_code="TVSA",
            residency_effective_date="2014-08-29",
            residency_description="Resident",
            contact_period_start="2017-03-15",
            marital_status="MRRD",
            marital_status_effective_date="2014-08-29",
            country_of_birth="NZ",
            expected_result_code="82701",
            expected_message="Transaction Unsuccessful",
            expected_subresult_code="82714",
            expected_subresult_message="Partner client number does not exist",
        ),
        build_row(
            condition="incorrect_partner_client_number_details",
            address_line2="Line2",
            suburb="Wellington",
            security_token_type="SYSTEM",
            ird_number="",
            partner_client_number="ABC123",
            partner_relationship_start_date="2014-08-29",
            # Important: this is intentionally blank for 82726.
            partner_from_type="",
            partner_to_type="PARTNER",
            residency_code="TVSA",
            residency_effective_date="2014-08-29",
            residency_description="Resident",
            contact_period_start="2017-03-15",
            marital_status="MRRD",
            marital_status_effective_date="2014-08-29",
            country_of_birth="NZ",
            expected_result_code="82701",
            expected_message="Transaction Unsuccessful",
            expected_subresult_code="82726",
            expected_subresult_message="Partner client number details are incomplete or incorrect",
        ),
        build_row(
            condition="invalid_residency_class_visa_status_date",
            residency_code="TVSA",
            residency_effective_date="2099-01-01",
            residency_description="Resident",
            contact_period_start="2017-03-15",
            security_token_type="USER",
            ird_number=None,
            marital_status="SNGL",
            marital_status_effective_date=None,
            expected_result_code="82701",
            expected_message="Transaction Unsuccessful",
            expected_subresult_code="82729",
            expected_subresult_message="Residency Class Visa Status change date cannot be before DOB or after system date",
        ),
        build_row(
            condition="partner_already_has_current_relationship",
            first_name=None,
            family_name=None,
            address_line2="Line2",
            suburb="Wellington",
            security_token_type="SYSTEM",
            ird_number="",
            partner_client_number="526286557",
            partner_relationship_start_date="2014-08-29",
            partner_from_type="PARTNER",
            partner_to_type="PARTNER",
            residency_code="TVSA",
            residency_effective_date="2014-08-29",
            residency_description="Resident",
            contact_period_start="2017-03-15",
            marital_status="MRRD",
            marital_status_effective_date="2014-08-29",
            country_of_birth="NZ",
            expected_result_code="82701",
            expected_message="Transaction Unsuccessful",
            expected_subresult_code="80099",
            expected_subresult_message="Result not recognized:",
        ),
    ]

    column_names = ", ".join(SC827_COLUMNS)
    placeholders = ", ".join(f":{column}" for column in SC827_COLUMNS)

    cur.executemany(
        f"""
        INSERT OR REPLACE INTO SC827 (
            {column_names}
        )
        VALUES (
            {placeholders}
        )
        """,
        rows,
    )


def insert_partner_pool_values(cur):
    """
    Optional:
    Add comma-separated partner client numbers using env variable:

      SC827_PARTNER_CLIENT_NUMBERS=511111111,522222222,533333333

    These should be clean D11 partner client numbers that are:
      - existing clients
      - not secured
      - not already linked in current partner relationship
    """

    partner_numbers_raw = os.getenv("SC827_PARTNER_CLIENT_NUMBERS", "").strip()

    if not partner_numbers_raw:
        print("No SC827_PARTNER_CLIENT_NUMBERS env variable supplied. Skipping partner pool insert.")
        return

    partner_numbers = [value.strip() for value in partner_numbers_raw.split(",") if value.strip()]

    cur.executemany(
        """
        INSERT OR IGNORE INTO SC827_PARTNER_POOL (
            environment,
            partner_client_number,
            status,
            notes
        )
        VALUES (
            'dev11',
            ?,
            'AVAILABLE',
            'SC827 positive partner scenario pool'
        )
        """,
        [(number,) for number in partner_numbers],
    )

    print(f"Inserted/confirmed {len(partner_numbers)} partner pool value(s).")


def print_verification(cur):
    print("\nSC827 endpoints:")
    cur.execute("""
        SELECT SERVICE_CONTRACT, SYSTEM, PATH
        FROM ENDPOINTS
        WHERE SERVICE_CONTRACT = 'SC827'
        ORDER BY SYSTEM
    """)

    for row in cur.fetchall():
        print(row)

    print("\nSC827 scenario rows:")
    cur.execute("""
        SELECT condition,
               partner_client_number,
               marital_status,
               residency_description,
               contact_period_start,
               security_token_type,
               expected_result_code,
               expected_message,
               expected_subresult_code,
               expected_subresult_message
        FROM SC827
        ORDER BY condition
    """)

    for row in cur.fetchall():
        print(row)

    print("\nSC827 partner pool status:")
    cur.execute("""
        SELECT status, COUNT(*)
        FROM SC827_PARTNER_POOL
        GROUP BY status
        ORDER BY status
    """)

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No partner pool values inserted yet.")


def main():
    conn = connect_db()
    cur = conn.cursor()

    add_sc827_endpoints(cur)
    create_sc827_table(cur)
    ensure_sc827_columns(cur)
    create_sc827_partner_pool_table(cur)
    insert_sc827_rows(cur)
    insert_partner_pool_values(cur)

    conn.commit()

    print_verification(cur)

    conn.close()
    print("\nSC827 DB setup completed successfully.")


if __name__ == "__main__":
    main()
