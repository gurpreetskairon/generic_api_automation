import csv
import json
import os
import random
import re
import sqlite3
import logging
import copy
import string
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo
import pytest

from apps.services.integration_soap.payload_data.dp603 import headers_iib
from utils.common_utils.helper_functions.other_helper_functions import generate_ird_number
from utils.oracledb.egw.egw_db_sql import get_next_pc_insert_into_db
import apps.services.integration_soap.payload_data as payloads
from apps.services.integration_soap.payload_data.sc811_v1 import get_payload_sc811_v1
from apps.services.integration_soap.payload_data.sc811_v2 import get_payload_sc811_v2
from apps.services.integration_soap.payload_data.sc828 import get_payload_sc828
from apps.services.integration_soap.soap_helpers import get_base64_encoded_string, get_token
from default_config import ENVIRONMENT
from utils.api_utils.helper.api_endpoint_builders import build_api_endpoint
from utils.common_utils.helper_functions.xml_parser import replace_tag, replace_tag_value
from utils.oracledb.swiftt.queries.swiftt_db_queries import sc806_client_with_debt_query
from utils.oracledb.swiftt.queries import swiftt_db_queries
from utils.oracledb.swiftt.swiftt_db_sql import get_from_swiftt, get_swiftt_connection_string
import xml.etree.ElementTree as et
from utils.sqlite.SqliteConnection import SqliteConnection

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DB_PATH = str(_PROJECT_ROOT / "Service_contract_data.db")


def sc151_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC151", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC151 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    client_number = client_number.zfill(9) if client_number else ""

    transaction_id = None if condition == "missing_transaction_id" else str(pytest.AUTO_TRANSACTION_ID)
    source_system = None if condition == "missing_source_system" else payloads.sc151.SC151_SOURCE_SYSTEM
    client_number = None if condition == "missing_client_number" else client_number

    return {
        "params": payloads.sc151.get_params_sc151(
            client_number=client_number, transaction_id=transaction_id, source_system=source_system
        ),
        "header": payloads.sc151.get_headers_sc151(),
        "raise_on_error": condition.startswith("successful_"),
    }


def dp151_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="DP151", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No DP151 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    client_number = client_number.zfill(9) if client_number else ""

    client_number = None if condition == "missing_client_number" else client_number
    transaction_id = None if condition == "missing_transaction_id" else str(pytest.AUTO_TRANSACTION_ID)
    source_system = None if condition == "missing_source_system" else payloads.dp151.DP151_SOURCE_SYSTEM

    return {
        "params": payloads.dp151.get_params_dp151(
            client_number=client_number, transaction_id=transaction_id, source_system=source_system
        ),
        "header": payloads.dp151.get_headers_dp151(),
        "raise_on_error": condition.startswith("successful_"),
    }


def sc153_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC153", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC153 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    participant_id = client_number.zfill(9) if client_number else ""

    username = payloads.sc153.SC153_INVALID_USERNAME if condition == "unauthorised" else payloads.sc153.SC153_USERNAME

    return {
        "condition": condition,
        "participant_id": participant_id,
        "header": payloads.sc153.get_headers_sc153(username=username),
        "raise_on_error": condition == "successful_response"
    }


def dp153_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="DP153", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No DP153 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    participant_id = client_number.zfill(9) if client_number else ""

    username = payloads.dp153.DP153_INVALID_USERNAME if condition == "unauthorised" else payloads.dp153.DP153_USERNAME

    return {
        "participant_id": participant_id,
        "header": payloads.dp153.get_headers_dp153(username=username),
        "raise_on_error": condition == "successful_response"
    }


def sc154_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC154", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC154 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    upskilling_id = str(scenario_data[4]).strip() if scenario_data[4] is not None else ""
    course_id = str(scenario_data[5]).strip() if scenario_data[5] is not None else ""
    course_name = str(scenario_data[6]).strip() if scenario_data[6] is not None else ""
    hours_completed = int(scenario_data[7])
    minutes_completed = int(scenario_data[8])

    return {
        "participant_id": client_number.zfill(9) if client_number else "",
        "upskilling_id": upskilling_id,
        "request_body": payloads.sc154.get_payload_sc154(
            course_id=course_id,
            course_name=course_name,
            hours_completed=hours_completed,
            minutes_completed=minutes_completed
        ),
        "header": payloads.sc154.get_headers_sc154(),
        "raise_error": False
    }


def dp154_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="DP154", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No DP154 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    participant_id = client_number.zfill(9) if client_number else ""
    upskilling_id = str(scenario_data[4]).strip() if scenario_data[4] is not None else ""
    course_id = str(scenario_data[5]).strip() if scenario_data[5] is not None else ""
    course_name = str(scenario_data[6]).strip() if scenario_data[6] is not None else ""
    hours_completed = int(scenario_data[7])
    minutes_completed = int(scenario_data[8])

    return {
        "participant_id": participant_id,
        "upskilling_id": upskilling_id,
        "request_body": payloads.dp154.get_payload_dp154(course_id, course_name, hours_completed, minutes_completed),
        "header": payloads.dp154.get_headers_dp154(),
        "raise_error": False
    }


def sc161_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC161", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC161 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    participant_id = client_number.zfill(9) if client_number else ""
    username = payloads.sc161.SC161_INVALID_USERNAME if condition == "unauthorised" else payloads.sc161.SC161_USERNAME

    return {
        "participant_id": participant_id,
        "header": payloads.sc161.get_headers_sc161(username=username),
        "raise_on_error": condition == "successful_response"
    }


def dp161_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="DP161", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No DP161 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    participant_id = client_number.zfill(9) if client_number else ""
    username = payloads.dp161.DP161_INVALID_USERNAME if condition == "unauthorised" else payloads.dp161.DP161_USERNAME

    return {
        "participant_id": participant_id,
        "header": payloads.dp161.get_headers_dp161(username=username),
        "raise_on_error": condition == "successful_response"
    }


def sc263_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC263", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC263 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    token_type = str(scenario_data[4]).strip() if scenario_data[4] is not None else ""

    username = "invalid_user" if condition == "authentication_failed" else payloads.sc263.SC263_USERNAME

    return {
        "client_number": client_number.zfill(9) if client_number else "",
        "token_type": token_type,
        "header": payloads.sc263.get_headers_sc263(username=username),
        "raise_on_error": condition == "successful_response"
    }


def sc264_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC264", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC264 test data was found for condition: {condition}")

    client_number = str(scenario_data[3]).strip() if scenario_data[3] is not None else ""
    token_type = str(scenario_data[4]).strip() if scenario_data[4] is not None else ""
    status = str(scenario_data[5]).strip() if scenario_data[5] is not None else ""

    username = "invalid_user" if condition == "authentication_failed" else payloads.sc264.SC264_USERNAME

    return {
        "client_number": client_number.zfill(9) if client_number else "",
        "token_type": token_type,
        "request_body": payloads.sc264.get_payload_sc264(status),
        "header": payloads.sc264.get_headers_sc264(username=username),
        "raise_on_error": condition == "successful_response"
    }


def sc512_payload_setup(condition="successful_payment_validation"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC512", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC512 test data was found in SQLite for condition: {condition}")

    card_number = scenario_data[3]
    payment_amount = scenario_data[4]
    payment_expiry_date = scenario_data[5]
    second_payment_amount = scenario_data[6]
    second_payment_expiry_date = scenario_data[7]

    correlation_id = str(uuid.uuid4())
    date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    schema_fault_conditions = {"invalid_xml"}

    return {
        "request_body": payloads.sc512.get_payload_sc512(
            correlation_id=correlation_id,
            date_time=date_time,
            card_number=card_number,
            payment_amount=payment_amount,
            payment_expiry_date=payment_expiry_date,
            second_payment_amount=second_payment_amount,
            second_payment_expiry_date=second_payment_expiry_date
        ),
        "header": payloads.sc512.get_headers_sc512(),
        "card_number": card_number,
        "correlation_id": correlation_id,
        "condition": condition,
        "raise_error": condition not in schema_fault_conditions
    }


def _get_sc531_sqlite_data(condition):
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(
            table_name="SC531", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC531 test data found in SQLite for condition: {condition}")

    return {
        "client_number": str(data[3]) if data[3] is not None else None,
        "username_token": data[4],
        "system_login": data[5],
        "created_by_user": data[6],
        "success": str(data[7]).lower() == "true"
    }


def _get_sc531_reapplication_clients(condition):
    if condition in ("successful_reapplication", "unsuccessful_reapplication"):
        query = swiftt_db_queries.SC531_52_WEEK_REAPP_CLIENT
    elif condition in ("successful_reapplication_suspended", "unsuccessful_reapplication_suspended"):
        query = swiftt_db_queries.SC531_SUSPENDED_52_WEEK_REAPP_CLIENT
    else:
        raise ValueError(f"Unsupported SC531 reapplication condition: {condition}")

    results = get_from_swiftt(get_swiftt_connection_string(), query)

    if not results or len(results) < 2:
        raise ValueError(f"Two eligible SC531 clients are required for condition: {condition}")

    return str(results[0][0]).zfill(9), str(results[1][0]).zfill(9)


def sc531_payload_setup(condition="successful_reapplication"):
    SC531_REAPPLICATION_CONDITIONS = {
        "successful_reapplication",
        "unsuccessful_reapplication",
        "successful_reapplication_suspended",
        "unsuccessful_reapplication_suspended"
    }
    correlation_id = str(uuid.uuid4())

    if condition in SC531_REAPPLICATION_CONDITIONS:
        iib_client_number, azure_client_number = _get_sc531_reapplication_clients(condition)
        username_token = "curamsystemuser"
        system_login = "CIMAY"
        created_by_user = "curamsystemuser"
        success = condition in ("successful_reapplication", "successful_reapplication_suspended")

        iib_request_body = payloads.sc531.get_payload_sc531(
            client_number=iib_client_number,
            username_token=username_token,
            system_login=system_login,
            created_by_user=created_by_user,
            success=success,
            correlation_id=correlation_id
        )

        azure_request_body = payloads.sc531.get_payload_sc531(
            client_number=azure_client_number,
            username_token=username_token,
            system_login=system_login,
            created_by_user=created_by_user,
            success=success,
            correlation_id=correlation_id
        )

    else:
        data = _get_sc531_sqlite_data(condition)
        iib_client_number = azure_client_number = data["client_number"]

        request_body = payloads.sc531.get_payload_sc531(
            client_number=iib_client_number,
            username_token=data["username_token"],
            system_login=data["system_login"],
            created_by_user=data["created_by_user"],
            success=data["success"],
            correlation_id=correlation_id
        )

        iib_request_body = azure_request_body = request_body

    return {
        "iib_request_body": iib_request_body,
        "azure_request_body": azure_request_body,
        "header": payloads.sc531.get_headers_sc531(),
        "iib_client_number": iib_client_number,
        "azure_client_number": azure_client_number,
        "condition": condition,
        "raise_error": condition != "user_not_recognised"
    }


def sc532_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc532_data = db.get_data(
            table_name="SC532", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc532_data:
        raise ValueError(f"No SC532 test data was found in SQLite for condition: {condition}")

    client_number, active_only_value, product_type_codes_value, service_lines_value = sc532_data[3:7]

    active_only_key = "" if active_only_value is None else str(active_only_value).strip().lower()
    active_only_options = {"": None, "none": None, "null": None, "not_set": None, "true": True, "false": False}

    if active_only_key not in active_only_options:
        raise ValueError(f"Unsupported SC532 ACTIVE_ONLY value '{active_only_value}' for condition: {condition}")

    product_type_codes = (
        [value.strip() for value in str(product_type_codes_value).split(",") if value.strip()]
        if product_type_codes_value
        else None
    )

    service_lines = (
        [value.strip() for value in str(service_lines_value).split(",") if value.strip()]
        if service_lines_value
        else None
    )

    return {
        "request_body": payloads.sc532.get_payload_sc532(
            client_number=client_number,
            active_only=active_only_options[active_only_key],
            product_type_codes=product_type_codes,
            service_lines=service_lines
        ),
        "header": payloads.sc532.get_headers_sc532()
    }


def sc547_payload_setup(condition="successful_payment_update"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC547", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC547 test data was found in SQLite for condition: {condition}")

    card_number = scenario_data[3]
    payment_amount = scenario_data[4]
    payment_expiry_date = scenario_data[5]
    debit_account_code = scenario_data[6]
    reconciliation_reference = scenario_data[7]
    source_payment_reference = scenario_data[8]

    correlation_id = str(uuid.uuid4())
    date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    schema_fault_conditions = {"invalid_xml"}

    return {
        "request_body": payloads.sc547.get_payload_sc547(
            correlation_id=correlation_id,
            date_time=date_time,
            card_number=card_number,
            payment_amount=payment_amount,
            payment_expiry_date=payment_expiry_date,
            debit_account_code=debit_account_code,
            reconciliation_reference=reconciliation_reference,
            source_payment_reference=source_payment_reference
        ),
        "header": payloads.sc547.get_headers_sc547(),
        "card_number": card_number,
        "correlation_id": correlation_id,
        "condition": condition,
        "raise_error": condition not in schema_fault_conditions
    }


def sc549_payload_setup(condition="successful_payment_card_update"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC549", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC549 test data was found in SQLite for condition: {condition}")

    client_number = scenario_data[3]
    card_number = scenario_data[4]
    expiry_date = scenario_data[5]
    pin_required = scenario_data[6]
    signature_required = scenario_data[7]
    blocked = scenario_data[8]
    blocked_reason = scenario_data[9]

    correlation_id = str(uuid.uuid4())
    date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    schema_fault_conditions = {"invalid_xml"}

    return {
        "request_body": payloads.sc549.get_payload_sc549(
            correlation_id=correlation_id,
            date_time=date_time,
            client_number=client_number,
            card_number=card_number,
            expiry_date=expiry_date,
            pin_required=pin_required,
            signature_required=signature_required,
            blocked=blocked,
            blocked_reason=blocked_reason
        ),
        "header": payloads.sc549.get_headers_sc549(),
        "client_number": client_number,
        "card_number": card_number,
        "correlation_id": correlation_id,
        "condition": condition,
        "raise_error": condition not in schema_fault_conditions
    }


def sc575_payload_setup(field=None, conditions="match"):
    env = os.getenv("API_TEST_ENV", "d11")

    test_data = payloads.sc575.SC575_TEST_DATA.get(env, {}).get(conditions)

    if test_data:
        ird_number = test_data["ird_number"]
        formatted_name = test_data["formatted_name"]
        date_of_birth = test_data["date_of_birth"]
        formatted_address = test_data["formatted_address"]
        user_id = test_data["user_id"]
    else:
        default_data = payloads.sc575.SC575_TEST_DATA[env]["match"]
        ird_number = default_data["ird_number"]
        formatted_name = default_data["formatted_name"]
        date_of_birth = default_data["date_of_birth"]
        formatted_address = default_data["formatted_address"]
        user_id = default_data["user_id"]

    audit_id = str(uuid4())
    correlation_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")
    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = payloads.sc575.get_payload_sc575(
        audit_id=audit_id,
        correlation_id=correlation_id,
        request_date_time=request_date_time,
        ird_number=ird_number,
        formatted_name=formatted_name,
        date_of_birth=date_of_birth,
        formatted_address=formatted_address,
        user_id=user_id
    )

    header = {"Content-Type": "text/xml; charset=utf-8", "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")}

    if conditions in ["match", "no_match_name", "no_match_dateOfBirth", "invalid_customer_type_ird"]:
        pass

    elif field == "IRD" and conditions == "number less than 9 digits":
        body = re.sub(r"(<v14:identifier>)(.*?)(</v14:identifier>)", r"\g<1>12345678\g<3>", body, flags=re.DOTALL)

    elif field == "IRD" and conditions == "number more than 9 digits":
        body = re.sub(r"(<v14:identifier>)(.*?)(</v14:identifier>)", r"\g<1>1234567890\g<3>", body, flags=re.DOTALL)

    elif field == "IRD" and conditions == "blank value":
        body = re.sub(r"(<v14:identifier>)(.*?)(</v14:identifier>)", r"\g<1>\g<3>", body, flags=re.DOTALL)

    elif field == "IRD" and conditions == "identifier block removed":
        body = replace_tag(xml_string=body, tag_to_replace="v13:identity")

    elif field == "name" and conditions == "blank value":
        body = re.sub(r"(<v14:formattedName>)(.*?)(</v14:formattedName>)", r"\g<1>\g<3>", body, flags=re.DOTALL)

    elif field == "name" and conditions == "name block removed":
        body = replace_tag(xml_string=body, tag_to_replace="v14:name")

    elif field == "address" and conditions == "blank value":
        body = re.sub(r"(<v16:formattedAddress>)(.*?)(</v16:formattedAddress>)", r"\g<1>\g<3>", body, flags=re.DOTALL)

    elif conditions == "invalid transactionId format":
        body = re.sub(
            r"(<v11:transactionId>)(.*?)(</v11:transactionId>)",
            r"\g<1>INVALID_TRANSACTION_ID\g<3>",
            body,
            flags=re.DOTALL
        )

    elif conditions == "blank transactionId":
        body = re.sub(r"(<v11:transactionId>)(.*?)(</v11:transactionId>)", r"\g<1>\g<3>", body, flags=re.DOTALL)

    elif conditions == "removed transactionId block":
        body = replace_tag(xml_string=body, tag_to_replace="v11:transactionId")

    elif conditions == "invalid username":
        body = body.replace("curamuser", "invaliduser")

    elif conditions == "blank username":
        body = re.sub(r"(<wsse:Username>)(.*?)(</wsse:Username>)", r"\g<1>\g<3>", body, flags=re.DOTALL)

    elif conditions == "removed username block":
        body = replace_tag(xml_string=body, tag_to_replace="wsse:Username")

    elif conditions == "invalid password":
        body = body.replace("REPLACE_PASSWORD", "invalidpassword")

    elif conditions == "blank password":
        body = re.sub(r"(<wsse:Password>)(.*?)(</wsse:Password>)", r"\g<1>\g<3>", body, flags=re.DOTALL)

    elif conditions == "removed password block":
        body = replace_tag(xml_string=body, tag_to_replace="wsse:Password")

    elif conditions == "invalid SOAPAction":
        header["SOAPAction"] = ""

    elif conditions == "missing SOAPAction":
        del header["SOAPAction"]

    else:
        raise ValueError(f"Invalid SC575 condition: {conditions}")

    payload = {"request_body": body, "header": header}
    return payload


def sc558_payload_setup(condition="successful_payment_details"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC558", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC558 test data was found in SQLite for condition: {condition}")

    source_payment_reference = scenario_data[3]
    correlation_id = str(uuid.uuid4())
    date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    schema_fault_conditions = {"invalid_xml"}

    return {
        "request_body": payloads.sc558.get_payload_sc558(
            correlation_id=correlation_id, date_time=date_time, source_payment_reference=source_payment_reference
        ),
        "header": payloads.sc558.get_headers_sc558(),
        "source_payment_reference": source_payment_reference,
        "correlation_id": correlation_id,
        "condition": condition,
        "raise_error": condition not in schema_fault_conditions
    }


def sc559_payload_setup(condition="successful_expired_payment"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC559", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC559 test data was found in SQLite for condition: {condition}")

    amount_spent = scenario_data[3]
    expiry_notified_date = scenario_data[4]
    source_payment_reference = scenario_data[5]

    correlation_id = str(uuid.uuid4())
    date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    schema_fault_conditions = {"invalid_xml"}

    return {
        "request_body": payloads.sc559.get_payload_sc559(
            correlation_id=correlation_id,
            date_time=date_time,
            amount_spent=amount_spent,
            expiry_notified_date=expiry_notified_date,
            source_payment_reference=source_payment_reference
        ),
        "header": payloads.sc559.get_headers_sc559(),
        "source_payment_reference": source_payment_reference,
        "condition": condition,
        "raise_error": condition not in schema_fault_conditions
    }


def sc805_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc805_data = db.get_data(
            table_name="SC805", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc805_data:
        raise ValueError(f"No SC805 test data was found in SQLite for condition: {condition}")

    client_number = sc805_data[3]
    payment_reference = sc805_data[4]

    return {
        "request_body": payloads.sc805.get_payload_sc805(client_number, payment_reference),
        "header": payloads.sc805.get_headers_sc805()
    }


def _get_sc806_sqlite_client(condition):
    db = SqliteConnection()
    db.connect()

    try:
        sc806_data = db.get_data(
            table_name="SC806", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc806_data:
        raise ValueError(f"No SC806 fallback data was found in SQLite for condition: {condition}")

    return str(sc806_data[3])


def _get_sc806_client_with_debt():
    results = get_from_swiftt(get_swiftt_connection_string(), sc806_client_with_debt_query)

    if not results:
        return None

    return str(results[0][0]).zfill(9)


def sc806v2_payload_setup(condition="successful_response"):
    if condition == "successful_response":
        client_number = _get_sc806_client_with_debt()

        if not client_number:
            logging.warning(
                "No eligible SC806 debt client was found through SWIFTT SQL. Using the verified SQLite fallback client."
            )
            client_number = _get_sc806_sqlite_client(condition)

    elif condition == "no_matching_record":
        client_number = _get_sc806_sqlite_client(condition)

    else:
        raise ValueError(f"Unsupported SC806 condition: {condition}")

    return {
        "request_body": payloads.sc806.get_payload_sc806(client_number),
        "header": payloads.sc806.get_headers_sc806()
    }


def sc807_payload_setup(condition="successful_debt_only"):
    db = SqliteConnection()
    db.connect()

    try:
        sc807_data = db.get_data(
            table_name="SC807", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc807_data:
        raise ValueError(f"No SC807 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc807.get_payload_sc807(
            client_number=sc807_data[3],
            product_id=sc807_data[4],
            breach_type_code=sc807_data[5],
            debt_status_code=sc807_data[6],
            debt_type_code=sc807_data[7],
            original_balance=sc807_data[8],
            recovery_status_code=sc807_data[9],
            comment=sc807_data[10],
            is_debt_non_taxable=sc807_data[11]
        ),
        "header": payloads.sc807.get_headers_sc807()
    }


def sc808_payload_setup(condition="successful_bank_account_search"):
    db = SqliteConnection()
    db.connect()

    try:
        sc808_data = db.get_data(
            table_name="SC808", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc808_data:
        raise ValueError(f"No SC808 test data was found in SQLite for condition: {condition}")

    search_type = sc808_data[3]

    if search_type == "bank_account":
        return {
            "request_body": payloads.sc808.get_payload_sc808(
                search_type=search_type,
                account_holder_name=sc808_data[4] or "test data",
                bank=sc808_data[5],
                branch=sc808_data[6],
                account=sc808_data[7],
                suffix=sc808_data[8]
            ),
            "header": payloads.sc808.get_headers_sc808()
        }

    if search_type == "community_service_card":
        return {
            "request_body": payloads.sc808.get_payload_sc808(search_type=search_type, card_number=sc808_data[9]),
            "header": payloads.sc808.get_headers_sc808()
        }

    raise ValueError(f"Unsupported SC808 search type '{search_type}' for condition: {condition}")


def sc814_payload_setup(condition="successful_paycycle_0"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC814", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC814 test data was found in SQLite for condition: {condition}")

    start_date = scenario_data[3]
    end_date = scenario_data[4]
    paycycle_code = scenario_data[5]
    country_codes = [code.strip() for code in str(scenario_data[6]).split(",") if code.strip()]

    audit_id = str(uuid.uuid4())
    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    schema_fault_conditions = {"invalid_paycycle_code"}

    return {
        "request_body": payloads.sc814.get_payload_sc814(
            audit_id=audit_id,
            request_date_time=request_date_time,
            start_date=start_date,
            end_date=end_date,
            paycycle_code=paycycle_code,
            country_codes=country_codes
        ),
        "header": payloads.sc814.get_headers_sc814(),
        "audit_id": audit_id,
        "paycycle_code": paycycle_code,
        "country_codes": country_codes,
        "condition": condition,
        "raise_error": condition not in schema_fault_conditions
    }


def sc823_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc823_data = db.get_data(
            table_name="SC823", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc823_data:
        raise ValueError(f"No SC823 test data was found in SQLite for condition: {condition}")

    client_number = sc823_data[3]
    note_text = sc823_data[4]
    short_description = sc823_data[5]
    case_event_id = sc823_data[6]
    note_id = sc823_data[7]

    schema_fault_conditions = {
        "invalid_action",
        "note_text_over_4000_characters",
        "note_text_with_special_characters",
        "short_description_over_100_characters",
        "short_description_with_special_characters"
    }

    return {
        "request_body": payloads.sc823.get_payload_sc823(
            client_number=client_number,
            note_text=note_text,
            short_description=short_description,
            case_event_id=case_event_id,
            note_id=note_id,
            condition=condition
        ),
        "header": payloads.sc823.get_headers_sc823(),
        "raise_error": condition not in schema_fault_conditions
    }


def sc825_payload_setup(conditions=None, bulk_test=False, bulk_swn=""):
    client_conditions = {
        "not_secured",
        "global_access",
        "temporary_access",
        "no_client_access",
        "no_matching_client",
        "user_not_found",
        "invalid SOAPAction",
        "missing SOAPAction"
    }
    db_conn = SqliteConnection()
    db_conn.connect()

    if conditions in client_conditions:
        data = db_conn.get_data("SC825", {"CONDITION": conditions})
    else:
        data = db_conn.get_data("SC825", {"CONDITION": None})
    db_conn.close()
    if bulk_test:
        client_id = bulk_swn
        user_id = "tbau0005"
    else:
        if data is None:
            raise Exception("SC825 payload setup failed, no suitable data found in local db")
        else:
            client_id = data[1]
            user_id = data[2]

    body = payloads.sc825.get_payload_sc825(client_id=client_id)
    header = payloads.sc825.get_headers_sc825()

    audit_id = str(uuid4())
    transaction_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")
    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = replace_tag_value(body, "auditId", audit_id)
    body = replace_tag_value(body, "transactionId", transaction_id)
    body = replace_tag_value(body, "requestDateTime", request_date_time)

    body = replace_tag_value(body, "id", user_id)
    if conditions is not None:
        if conditions == "missing header":
            body = replace_tag(xml_string=body, tag_to_replace="soapenv:Header")
        elif conditions == "invalid credentials":
            body = body.replace("curamsystemuser", "userofcuramsystem")
        elif conditions == "missing security token":
            body = replace_tag(xml_string=body, tag_to_replace="v11:securityToken")
        elif conditions == "invalid security token":
            body = body.replace("rwohl001", "001rwohl")
        elif conditions == "missing interaction pattern":
            body = replace_tag(xml_string=body, tag_to_replace="v11:interactionPattern")
        elif conditions == "invalid interaction pattern":
            body = body.replace("REQUEST_RESPONSE", "RESPONSE_REQUEST")
        elif conditions == "invalid client":
            body = body.replace(client_id, "000000000")
        elif conditions == "missing client":
            body = replace_tag(xml_string=body, tag_to_replace="v14:identifier")
        elif conditions == "invalid SOAPAction":
            header["SOAPAction"] = ""
        elif conditions == "missing SOAPAction":
            del header["SOAPAction"]
        elif conditions == "no Security information":
            body = replace_tag(xml_string=body, tag_to_replace="wsse:UsernameToken")
    payload = {"request_body": body, "header": header}
    return payload


def _get_sc827_request_date_time():
    return datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S")


def _get_sc827_random_alpha_value(prefix, length=6):
    """
    Returns alpha-only random value.

    SC827 person name format should be alpha characters only.
    Avoid numbers/special characters for positive scenarios.
    """

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_part = "".join(random.choices(alphabet, k=length))
    return f"{prefix}{random_part}"


def _get_sc827_value_or_random(data, key, prefix):
    """
    Uses DB value when it is provided.

    Generates a random value only when the DB value is NULL.

    Important:
    Do not use `or` here because an empty string is valid test data
    for some negative scenarios.
    """

    value = data.get(key)

    if value is None:
        return _get_sc827_random_alpha_value(prefix)

    return value


def _get_sc827_condition_data(condition):
    """
    Reads SC827 test data from local SQLite table SC827.
    """

    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT *
            FROM SC827
            WHERE condition = ?
            """,
            (condition,)
        )

        row = cur.fetchone()

    finally:
        conn.close()

    if not row:
        raise ValueError(
            f"No SC827 test data found for condition '{condition}' in Service_contract_data.db table SC827."
        )

    return dict(row)


def _get_available_sc827_partner_client_number(condition, transaction_id):
    """
    Gets one AVAILABLE partner client number from SC827_PARTNER_POOL
    and marks it as RESERVED.

    This is needed because partner client numbers are consumable test data.
    Once a successful SC827 client-with-partner request links the partner,
    the same partner client number should not be reused for another positive run.
    """

    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("BEGIN IMMEDIATE")

        cur.execute(
            """
            SELECT id, partner_client_number
            FROM SC827_PARTNER_POOL
            WHERE status = 'AVAILABLE'
            ORDER BY id
            LIMIT 1
            """
        )

        row = cur.fetchone()

        if not row:
            raise ValueError(
                "No AVAILABLE partner client number found in SC827_PARTNER_POOL. "
                "Please add more unlinked/unconsumed partner client numbers."
            )

        pool_id, partner_client_number = row

        cur.execute(
            """
            UPDATE SC827_PARTNER_POOL
            SET status = 'RESERVED',
                used_for_condition = ?,
                reserved_transaction_id = ?,
                reserved_at = datetime('now')
            WHERE id = ?
            """,
            (condition, transaction_id, pool_id)
        )

        conn.commit()

        return {"pool_id": pool_id, "partner_client_number": partner_client_number}

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def mark_sc827_partner_client_number_used(pool_id, created_client_number=None):
    """
    Marks reserved partner client number as USED after SC827 returns success.

    Call this from the SC827 step file after validating that a generated
    clientNumber exists in the successful response.
    """

    if not pool_id:
        return

    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE SC827_PARTNER_POOL
            SET status = 'USED',
                created_client_number = ?,
                used_at = datetime('now')
            WHERE id = ?
            """,
            (created_client_number, pool_id)
        )

        conn.commit()

    finally:
        conn.close()


def sc827_payload_setup(condition=None):
    """
    Builds SC827 Register Client payload.

    Supported positive conditions:
      - valid_register_client_without_partner
      - valid_register_client_with_partner

    Data source:
      - Scenario data is read from local SQLite table SC827.
      - Partner client number for valid_register_client_with_partner is taken
        from SC827_PARTNER_POOL if partner_client_number is not fixed in SC827.

    Generated dynamically:
      - audit_id
      - transaction_id
      - request_date_time
      - first_name, only when first_name is NULL in DB
      - family_name, only when family_name is NULL in DB
    """

    if condition is None:
        condition = "valid_register_client_without_partner"

    data = _get_sc827_condition_data(condition)

    audit_id = str(uuid4())
    request_date_time = _get_sc827_request_date_time()

    first_name = _get_sc827_value_or_random(data, "first_name", "AUTO")
    family_name = _get_sc827_value_or_random(data, "family_name", "SC")

    if condition == "missing_mandatory_person_data":
        first_name = ""

    if condition == "invalid_person_name_format":
        first_name = "AUTO123"
        family_name = "SC123"

    if condition == "invalid_ird_number_format":
        data["ird_number"] = "ABC123"

    partner_pool_data = None
    partner_client_number = data.get("partner_client_number")

    if condition == "valid_register_client_with_partner" and not partner_client_number:
        partner_pool_data = _get_available_sc827_partner_client_number(
            condition=condition, transaction_id=pytest.AUTO_TRANSACTION_ID
        )
        partner_client_number = partner_pool_data["partner_client_number"]

    request_body = payloads.sc827.get_payload_sc827(
        audit_id=audit_id,
        request_date_time=request_date_time,
        user_id=data["user_id"],
        source_system=data.get("source_system", "SAL"),
        first_name=first_name,
        family_name=family_name,
        middle_name=data.get("middle_name", ""),
        date_of_birth=data["date_of_birth"],
        gender=data["gender"],
        address_line1=data["address_line1"],
        address_line2=data.get("address_line2", ""),
        suburb=data.get("suburb", ""),
        city=data["city"],
        post_code=data.get("post_code", ""),
        country_code=data.get("country_code", "NZ"),
        country_of_birth=data.get("country_of_birth", "NZ"),
        residency_code=data.get("residency_code"),
        residency_effective_date=data.get("residency_effective_date"),
        residency_description=data.get("residency_description"),
        ird_number=data.get("ird_number"),
        marital_status=data.get("marital_status"),
        marital_status_effective_date=data.get("marital_status_effective_date"),
        partner_client_number=partner_client_number,
        partner_relationship_start_date=data.get("partner_relationship_start_date"),
        partner_from_type=data.get("partner_from_type", "PARTNER"),
        partner_to_type=data.get("partner_to_type", "PARTNER"),
        contact_period_start=data.get("contact_period_start"),
        security_token_type=data.get("security_token_type", "USER")
    )

    header = {"Content-Type": "text/xml", "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")}

    return {
        "request_body": request_body,
        "header": header,
        "audit_id": audit_id,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "request_date_time": request_date_time,
        "first_name": first_name,
        "family_name": family_name,
        "condition": condition,
        "partner_client_number": partner_client_number,
        "partner_pool_id": partner_pool_data["pool_id"] if partner_pool_data else None,
        "expected_result_code": data.get("expected_result_code"),
        "expected_message": data.get("expected_message"),
        "expected_subresult_code": data.get("expected_subresult_code"),
        "expected_subresult_message": data.get("expected_subresult_message")
    }


def sc828_payload_setup(conditions="successful_response"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(table_name="SC828", column_names_and_values={"CONDITION": conditions})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC828 test data found in SQLite for condition: {conditions}")

    family_name = data[1]
    first_name = data[2]
    middle_names = data[3]
    date_of_birth = data[4]

    audit_id = str(uuid4())
    correlation_id = str(uuid4())
    request_datetime = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    body = get_payload_sc828(
        audit_id=audit_id,
        correlation_id=correlation_id,
        request_datetime=request_datetime,
        family_name=family_name,
        first_name=first_name,
        middle_names=middle_names,
        date_of_birth=date_of_birth
    )

    header = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "tns:inquire",
        "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")
    }

    payload = {"request_body": body, "header": header}
    return payload


def get_sc829_scenario_data(env, system=None, category_code=None, type_code=None, scenario_key=None):
    if scenario_key:
        return payloads.sc829.SC829_TEST_DATA[env][scenario_key]

    for scenario_data in payloads.sc829.SC829_TEST_DATA[env].values():
        if (
            scenario_data["source_system"].casefold() == system.casefold()
            and scenario_data["category_code"] == category_code
            and scenario_data["type_code"] == type_code
        ):
            return scenario_data

    raise ValueError(
        f"No SC829 test data found for system={system}, category_code={category_code}, type_code={type_code}"
    )


def sc829_payload_setup(
    system="WASP",
    conditions="correct",
    category_code=None,
    type_code=None,
    client_identifier=None,
    identity_type=None,
    scenario_key=None
):
    env = os.getenv("API_TEST_ENV", "d11")
    data = get_sc829_scenario_data(
        env=env, system=system, category_code=category_code, type_code=type_code, scenario_key=scenario_key
    )

    data = data.copy()

    if client_identifier:
        data["client_id"] = client_identifier

    if identity_type:
        data["identity_type"] = identity_type

    body = payloads.sc829.get_payload_sc829(username="mymsduser", password="password", scenario_data=data)

    header = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": '"tns:manage"', "MSD-Sub-Env": env}

    if conditions == "correct":
        pass
    elif conditions == "invalid client":
        pass
    elif conditions == "missing type code":
        body = replace_tag(xml_string=body, tag_to_replace="v15:type")

    elif conditions == "invalid type code":
        body = body.replace(data["type_code"], "INVALIDTYPE")

    elif conditions == "invalid category":
        body = body.replace(data["category_code"], "INVALIDCATEGORY")

    elif conditions == "business validation failed":
        body = body.replace(
            f"<v15:expectedEndDate>{data.get('expected_end_date')}</v15:expectedEndDate>",
            "<v15:expectedEndDate>2026-04-20</v15:expectedEndDate>"
        )

    elif conditions == "missing SOAPAction":
        del header["SOAPAction"]

    elif conditions == "invalid SOAPAction":
        header["SOAPAction"] = ""

    elif conditions == "no Security Information":
        body = replace_tag(xml_string=body, tag_to_replace="wsse:UsernameToken")

    else:
        raise ValueError(f"Invalid SC829 condition: {conditions}")

    return {"request_body": body, "header": header}


def sc830_payload_setup(condition=None, bulk_test: bool = False, bulk_swn: str = ""):
    """
    Creates SC830 SOAP request payload using test data from local SQLite database.

    This follows the same approach as SC825:
    - Read client/user/filter data from local DB table SC830
    - Generate audit_id, transaction_id and request_date_time dynamically
    - Build SC830 request body directly from sc830.get_payload_sc830()
    """

    client_conditions = {
        "has_tags_flags",
        "programme_tags_only",
        "client_flags_only",
        "no_current_programme_tags_and_flags",
        "no_current_programme_tags",
        "no_current_flags",
        "no_matching_client",
        "invalid_client_number",
        "missing_client_number",
        "user_not_recognised"
    }

    db_conn = SqliteConnection()
    db_conn.connect()

    if condition in client_conditions:
        data = db_conn.get_data("SC830", {"CONDITION": condition})
    else:
        data = db_conn.get_data("SC830", {"CONDITION": "has_tags_flags"})

    db_conn.close()

    if data is None:
        raise Exception("SC830 payload setup failed, no suitable data found in local db")
    if not bulk_test:
        client_id = data[1]
    else:
        client_id = bulk_swn
    user_id = data[2]
    source_system = "MyMSD"
    include_client_flags = "true"
    include_programme_tags = "true"

    audit_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")
    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = payloads.sc830.get_payload_sc830(
        audit_id=audit_id,
        request_date_time=request_date_time,
        client_id=client_id,
        user_id=user_id,
        source_system=source_system,
        include_client_flags=include_client_flags,
        include_programme_tags=include_programme_tags
    )

    header = {"Content-Type": "text/xml; charset=utf-8", "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")}

    payload = {
        "request_body": body,
        "header": header,
        "audit_id": audit_id,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "request_date_time": request_date_time,
        "client_id": client_id,
        "user_id": user_id,
        "source_system": source_system,
        "include_client_flags": include_client_flags,
        "include_programme_tags": include_programme_tags
    }

    return payload


def dp830_payload_setup(condition=None, bulk_test: bool = False, bulk_swn: str = ""):
    client_conditions = {
        "has_tags_flags",
        "programme_tags_only",
        "client_flags_only",
        "no_current_programme_tags_and_flags",
        "no_current_programme_tags",
        "no_current_flags",
        "no_matching_client",
        "invalid_client_number",
        "missing_client_number",
        "user_not_recognised"
    }

    db_conn = SqliteConnection()
    db_conn.connect()
    if condition in client_conditions:
        data = db_conn.get_data("SC830", {"CONDITION": condition})
    else:
        data = db_conn.get_data("SC830", {"CONDITION": "has_tags_flags"})
    db_conn.close()

    if data is None:
        raise Exception("SC830 payload setup failed, no suitable data found in local db")
    if not bulk_test:
        client_id = data[1]
    else:
        client_id = bulk_swn

    headers = payloads.dp830.dp830_headers()
    params = payloads.dp830.dp830_params(client_number=client_id)

    if condition == "user_not_recognised":
        headers = payloads.dp830.dp830_headers(user_string="bob:password")

    return headers, params


def sc841_payload_setup(condition="matching_address"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC841", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC841 test data was found in SQLite for condition: {condition}")

    address_id = None if condition == "invalid_request" else str(scenario_data[3])

    return {
        "request_body": payloads.sc841.get_payload_sc841(address_id=address_id),
        "header": payloads.sc841.get_headers_sc841(),
        "raise_error": True
    }


def sc842_payload_setup(condition="matching_postcode"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC842", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC842 test data was found in SQLite for condition: {condition}")

    line1 = str(scenario_data[3]) if scenario_data[3] is not None else ""
    line2 = str(scenario_data[4]) if scenario_data[4] else None
    suburb = str(scenario_data[5]) if scenario_data[5] else None
    city = str(scenario_data[6]) if scenario_data[6] else None

    return {
        "request_body": payloads.sc842.get_payload_sc842(line1=line1, line2=line2, suburb=suburb, city=city),
        "header": payloads.sc842.get_headers_sc842(),
        "raise_error": True
    }


def sc847_payload_setup(condition=None, bulk_test: bool = False, bulk_swn: str = ""):
    """
    Creates SC847 SOAP request payload using test data from local SQLite database.

    ```
    This follows the same approach as SC830:
    - Read client data from local DB table SC847
    - Generate audit_id, transaction_id and request_date_time dynamically
    - Build SC847 request body directly from sc847.get_payload_sc847()
    """

    client_conditions = {
        "active_dtrd",
        "dtrd_prescription_medication",
        "dtrd_receiving_treatment",
        "dtrd_awaiting_treatment",
        "dtrd_diagnosed_dependence",
        "dtrd_drug_obligation_failure",
        "dtrd_drug_help_required",
        "dtrd_drug_other",
        "dtrd_drug_medical_certificate",
        "dtrd_drug_no_good_sufficient_reason",
        "dtrd_drug_brief_interventions",
        "dtrd_drug_referred_assessment",
        "no_active_dtrd",
        "missing_client_number",
        "invalid_client_number"
    }

    db_conn = SqliteConnection()
    db_conn.connect()

    if condition in client_conditions:
        data = db_conn.get_data("SC847", {"CONDITION": condition})
    else:
        data = db_conn.get_data("SC847", {"CONDITION": "active_dtrd"})

    db_conn.close()

    if data is None:
        raise Exception("SC847 payload setup failed, no suitable data found in local db")

    if not bulk_test:
        client_id = data[1]
    else:
        client_id = bulk_swn
    expected_result_code = data[2]
    expected_result_message = data[3]
    type_code = data[4]
    type_description = data[5]
    effective_start = data[6]
    effective_end = data[7]

    source_system = "CMS"
    correlation_id = "correl123"
    security_token_id = "tbau0005"
    security_token_type = "USER"

    audit_id = str(uuid4())
    transaction_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")
    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = payloads.sc847.get_payload_sc847(
        client_id=client_id,
        audit_id=audit_id,
        request_date_time=request_date_time,
        correlation_id=correlation_id,
        source_system=source_system,
        security_token_id=security_token_id,
        security_token_type=security_token_type
    )

    header = {"Content-Type": "application/xml", "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")}

    payload = {
        "request_body": body,
        "header": header,
        "audit_id": audit_id,
        "transaction_id": transaction_id,
        "request_date_time": request_date_time,
        "client_id": client_id,
        "source_system": source_system,
        "correlation_id": correlation_id,
        "security_token_id": security_token_id,
        "security_token_type": security_token_type,
        "expected_result_code": expected_result_code,
        "expected_result_message": expected_result_message,
        "type_code": type_code,
        "type_description": type_description,
        "effective_start": effective_start,
        "effective_end": effective_end
    }

    return payload


def sc856_payload_setup(condition="pay_period_and_redirections"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC856", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC856 test data was found in SQLite for condition: {condition}")

    client_number = scenario_data[3]
    redirection_type_code = scenario_data[4]

    audit_id = str(uuid.uuid4())
    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    return {
        "request_body": payloads.sc856.get_payload_sc856(
            audit_id=audit_id,
            request_date_time=request_date_time,
            client_number=client_number,
            redirection_type_code=redirection_type_code
        ),
        "header": payloads.sc856.get_headers_sc856(),
        "client_number": client_number,
        "condition": condition
    }


def sc873_payload_setup(condition="normal_client"):
    db = SqliteConnection()
    db.connect()

    try:
        sc873_data = db.get_data(
            table_name="SC873", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc873_data:
        raise ValueError(f"No SC873 test data was found in SQLite for condition: {condition}")

    client_number = "" if sc873_data[3] is None else str(sc873_data[3])
    start_date = str(sc873_data[4])
    end_date = str(sc873_data[5])
    include_partner = sc873_data[6]

    return {
        "request_body": payloads.sc873.get_payload_sc873(
            client_number, start_date, end_date, include_partner, condition
        ),
        "header": payloads.sc873.get_headers_sc873()
    }


def _get_sc893_sqlite_client(condition):
    db = SqliteConnection()
    db.connect()

    try:
        sc893_data = db.get_data(
            table_name="SC893", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc893_data:
        raise ValueError(f"No SC893 test data was found in SQLite for condition: {condition}")

    return sc893_data[3]


def _get_sc893_tas_reapplication_client():
    results = get_from_swiftt(get_swiftt_connection_string(), swiftt_db_queries.SC893_TAS_REAPPLICATION_CLIENT)

    if not results:
        raise ValueError("No eligible TAS re-application client was found for SC893 through SWIFTT SQL")

    return str(results[0][0]).zfill(9)


def sc893_payload_setup(condition="successful_response"):
    if condition == "successful_response":
        client_number = _get_sc893_tas_reapplication_client()

    elif condition == "invalid_request":
        client_number = _get_sc893_sqlite_client(condition)

    else:
        raise ValueError(f"Unsupported SC893 condition: {condition}")

    return {
        "request_body": payloads.sc893.get_payload_sc893(client_number=client_number),
        "header": payloads.sc893.get_headers_sc893(),
        "raise_error": True
    }


def _get_dp893_sqlite_client(condition):
    db = SqliteConnection()
    db.connect()

    try:
        dp893_data = db.get_data(
            table_name="DP893", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not dp893_data:
        raise ValueError(f"No DP893 test data was found in SQLite for condition: {condition}")

    return dp893_data[3]


def _get_dp893_tas_reapplication_clients():
    results = get_from_swiftt(get_swiftt_connection_string(), swiftt_db_queries.SC893_TAS_REAPPLICATION_CLIENT)

    if not results or len(results) < 2:
        raise ValueError("At least two eligible TAS re-application clients are required for DP893 comparison testing")

    return str(results[0][0]).zfill(9), str(results[1][0]).zfill(9)


def dp893_payload_setup(condition="tas_reapplication_submitted"):
    headers = payloads.dp893.dp893_headers()
    headers["MSD-Sub-Env"] = "d11"
    params = payloads.dp893.dp893_params()

    if condition == "tas_reapplication_submitted":
        datapower_client, azure_client = _get_dp893_tas_reapplication_clients()

        datapower_request_body = payloads.dp893.dp893_request(business_key_identifier=datapower_client)
        azure_request_body = payloads.dp893.dp893_request(business_key_identifier=azure_client)

    elif condition == "invalid_request":
        client_number = _get_dp893_sqlite_client(condition)

        datapower_request_body = payloads.dp893.dp893_request(business_key_identifier=client_number)
        datapower_request_body.pop("application", None)

        azure_request_body = datapower_request_body.copy()

    elif condition == "invalid_client_info_changed":
        client_number = _get_dp893_sqlite_client(condition)

        datapower_request_body = payloads.dp893.dp893_request(business_key_identifier=client_number)
        azure_request_body = payloads.dp893.dp893_request(business_key_identifier=client_number)

        datapower_request_body["application"]["oneOffApplication"]["commentCategories"][0]["clientInfoChanged"] = ""

        azure_request_body["application"]["oneOffApplication"]["commentCategories"][0]["clientInfoChanged"] = ""

    else:
        raise ValueError(f"Unsupported DP893 condition: {condition}")

    raise_error = condition != "invalid_client_info_changed"

    return headers, params, datapower_request_body, azure_request_body, raise_error


def sc898_payload_setup(condition=None, bulk_test: bool = False, bulk_swn: str = ""):
    """
    Creates SC898 SOAP request payload using test data from local SQLite database.

    """

    client_conditions = {
        "active_c2e_flag",
        "expired_c2e_flag",
        "no_c2e_flag",
        "no_matching_client",
        "invalid_client_number",
        "missing_client_number",
        "user_not_recognised"
    }

    db_conn = SqliteConnection()
    db_conn.connect()

    if condition in client_conditions:
        data = db_conn.get_data("SC898", {"CONDITION": condition})
    else:
        data = db_conn.get_data("SC898", {"CONDITION": "active_c2e_flag"})

    db_conn.close()

    if data is None:
        raise Exception("SC898 payload setup failed, no suitable data found in local db")
    if not bulk_test:
        client_id = data[1]
    else:
        client_id = bulk_swn
    user_id = data[2]
    source_system = "MyMSD"
    include_c2e_flag = "true"

    audit_id = str(uuid4())
    transaction_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")
    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = payloads.sc898.get_payload_sc898(
        audit_id=audit_id,
        request_date_time=request_date_time,
        client_id=client_id,
        user_id=user_id,
        source_system=source_system,
        include_c2e_flag=include_c2e_flag
    )

    header = {"Content-Type": "application/xml", "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")}

    payload = {
        "request_body": body,
        "header": header,
        "audit_id": audit_id,
        "transaction_id": transaction_id,
        "request_date_time": request_date_time,
        "client_id": client_id,
        "user_id": user_id,
        "source_system": source_system,
        "include_c2e_flag": include_c2e_flag
    }

    return payload


import uuid


def dp603_payload_setup(swn, conditions="correct", azure=False):
    if azure:
        header = payloads.dp603.headers_azure()
    else:
        header = payloads.dp603.headers_iib()

    # Generate a unique transaction ID for every request
    header["transactionId"] = str(uuid.uuid4())

    header["x-jws-signature"] = get_token(swn, "dp603")

    if conditions == "missing authorization":
        del header["Authorization"]
    elif conditions == "invalid authorization":
        header["Authorization"] = "Basic c3123456YXNzd29yZA=="
    elif conditions == "missing transactionId":
        del header["transactionId"]
    elif conditions == "invalid transactionId":
        header["transactionId"] = "invalid-transaction-id"
    elif conditions == "missing sourceSystem":
        del header["sourceSystem"]
    elif conditions == "invalid sourceSystem":
        header["sourceSystem"] = "TEST"
    elif conditions == "missing requestDateTime":
        del header["requestDateTime"]
    elif conditions == "invalid requestDateTime":
        header["requestDateTime"] = "2020/10/20T12:34:56.456"
    elif conditions == "missing securityTokenId":
        del header["securityTokenId"]
    elif conditions == "invalid securityTokenId":
        header["securityTokenId"] = "UserID"
    elif conditions == "missing jws":
        del header["x-jws-signature"]
    elif conditions == "invalid jws key":
        header["x-jws-signature"] = f"{header['x-jws-signature']}-autotest"
    elif conditions == "invalid jws algorithm":
        header["x-jws-signature"] = get_token(swn, "dp603", algorithm="HS256")
    elif conditions == "invalid jws method":
        header["x-jws-signature"] = get_token(swn, "dp603", method="TRACE")
    elif conditions == "invalid query string":
        header["x-jws-signature"] = get_token(swn, "dp603", q_string="null")

    return header


def dp604_payload_setup(swn, conditions="correct", azure=False):
    params = payloads.dp604.dp604_params()

    if azure:
        header = payloads.dp604.headers_azure()
    else:
        header = payloads.dp604.headers_iib()

    # Generate a unique transaction ID for every request
    header["transactionId"] = str(uuid.uuid4())

    header["x-jws-signature"] = get_token(swn, "dp604")

    # Generate a new transaction ID for every request
    header["transactionId"] = str(uuid.uuid4())

    if conditions == "missing authorization":
        del header["Authorization"]
    elif conditions == "invalid authorization":
        header["Authorization"] = "Basic c3123456YXNzd29yZA=="
    elif conditions == "missing transactionId":
        del header["transactionId"]
    elif conditions == "invalid transactionId":
        header["transactionId"] = "invalid-transaction-id"
    elif conditions == "missing sourceSystem":
        del header["sourceSystem"]
    elif conditions == "invalid sourceSystem":
        header["sourceSystem"] = "TEST"
    elif conditions == "missing requestDateTime":
        del header["requestDateTime"]
    elif conditions == "invalid requestDateTime":
        header["requestDateTime"] = "09/03/2026"
    elif conditions == "missing securityTokenId":
        del header["securityTokenId"]
    elif conditions == "invalid securityTokenId":
        header["securityTokenId"] = "UserID"
    elif conditions == "missing usage":
        del params["usage"]
    elif conditions == "missing jws":
        del header["x-jws-signature"]
    elif conditions == "invalid jws key":
        header["x-jws-signature"] = f"{header['x-jws-signature']}-autotest"
    elif conditions == "invalid jws algorithm":
        header["x-jws-signature"] = get_token(swn, "dp604", algorithm="HS256")
    elif conditions == "invalid jws method":
        header["x-jws-signature"] = get_token(swn, "dp604", method="TRACE")
    elif conditions == "invalid query string":
        header["x-jws-signature"] = get_token(swn, "dp604", q_string="null")

    return header, params


def dp605_payload_setup(
    condition="valid_client",
    category_code="STAFFSECURITYALERT",
    type_code="LWAR",
    client_number=None,
    effective_start=None,
    effective_end=None,
    system="AZURE",
    subsystem=None
):
    env = os.getenv("API_TEST_ENV", "dev11").strip()

    if env.casefold() == "d11":
        env = "dev11"

    if system == "IIB" and subsystem is None:
        subsystem = "STAR"

    if system == "AZURE" and subsystem is None:
        subsystem = "NONE"

    data = get_dp605_scenario_data(env=env, condition=condition).copy()

    if client_number:
        data["client_number"] = str(client_number)

    data["client_number"] = str(data["client_number"])

    request_body = payloads.dp605.get_payload_dp605(
        category_code=category_code,
        type_code=type_code,
        effective_start=effective_start or data.get("effective_start"),
        effective_end=effective_end or data.get("effective_end")
    )

    request_body["condition"] = condition

    endpoint = build_api_endpoint("DP605", system=system, sub_system=subsystem)

    security_token_id = data.get("security_token_id") or "tbau0005"

    if system == "AZURE":
        header = payloads.dp605.headers_azure(security_token_id=security_token_id)
        endpoint = payloads.dp605.url_azure(endpoint=endpoint, payload=request_body, swn=str(data["client_number"]))

    elif system == "IIB" and subsystem == "STAR":
        header = payloads.dp605.headers_iib()
        endpoint = payloads.dp605.url_iib(endpoint=endpoint, payload=request_body, swn=str(data["client_number"]))

    else:
        raise ValueError(f"Invalid DP605 system/subsystem: system={system}, subsystem={subsystem}")

    header["x-jws-signature"] = get_token(str(data["client_number"]), "dp605")

    request_body.pop("condition", None)

    if condition not in ["valid_client", "invalid_client_number"]:
        raise ValueError(f"Invalid DP605 condition: {condition}")

    return {
        "endpoint_url": endpoint,
        "request_body": request_body,
        "header": header,
        "client_number": data["client_number"],
        "encoded_client_number": get_base64_encoded_string(str(data["client_number"])),
        "category_code": category_code,
        "type_code": type_code,
        "condition": condition,
        "security_token_id": security_token_id,
        "system": system,
        "subsystem": subsystem
    }


def get_dp605_scenario_data(env, condition):
    db = SqliteConnection()
    db.connect()

    identifier = {"ENV": env, "condition": condition}

    result = db.get_data(table_name="DP605", column_names_and_values=identifier)

    db.close()

    if result is None:
        raise ValueError(f"No DP605 test data found for ENV={env}, condition={condition}")

    return {
        "ENV": result[0],
        "client_number": result[1],
        "condition": result[2],
        "effective_start": result[3],
        "effective_end": result[4],
        "security_token_id": result[5]
    }


def dp606_payload_setup(conditions="correct", azure=False):
    if azure:
        header = payloads.dp606.headers_azure()
    else:
        header = payloads.dp606.headers_iib()

    if conditions == "missing auditID":
        del header["auditId"]
    elif conditions == "missing transactionId":
        del header["transactionId"]
    elif conditions == "missing sourceSystem":
        del header["sourceSystem"]
    elif conditions == "invalid sourceSystem":
        header["sourceSystem"] = "TEST"
    elif conditions == "missing requestDateTime":
        del header["requestDateTime"]
    elif conditions == "invalid requestDateTime":
        header["requestDateTime"] = "          "
    return header


def get_dp823_scenario_data(environment, condition):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="DP823", column_names_and_values={"ENVIRONMENT": environment, "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No DP823 test data found for ENVIRONMENT={environment}, CONDITION={condition}")

    return {
        "environment": scenario_data[1],
        "condition": scenario_data[2],
        "client_number": scenario_data[3],
        "note_text": scenario_data[4],
        "short_description": scenario_data[5]
    }


def dp823_payload_setup(condition="successful_response"):
    data = get_dp823_scenario_data("dev11", condition)

    if condition == "user_not_recognised":
        headers = payloads.dp823.dp823_headers(user_string="invalid_user:invalid_password")
    else:
        headers = payloads.dp823.dp823_headers()

    params = payloads.dp823.dp823_params()
    body = payloads.dp823.dp823_body(data["client_number"], data["note_text"], data["short_description"])

    raise_error = condition != "user_not_recognised"

    return headers, params, body, raise_error


def dp825_payload_setup(condition="valid_client", client_number=None, date_time=None):
    env = os.getenv("API_TEST_ENV", "dev11").strip()

    if env.casefold() == "d11":
        env = "dev11"

    valid_conditions = ["valid_client", "no_matching_client"]

    if condition not in valid_conditions:
        raise ValueError(f"Invalid DP825 condition: {condition}")

    data = get_dp825_scenario_data(env=env, condition=condition).copy()

    if client_number is not None:
        data["client_number"] = str(client_number)

    transaction_id = str(uuid4())

    return {
        "client_number": str(data["client_number"]),
        "transaction_id": transaction_id,
        "request_date_time": date_time,
        "iib_headers": payloads.dp825.headers_iib(request_date_time=date_time),
        "azure_headers": payloads.dp825.headers_azure(request_date_time=date_time),
        "condition": condition
    }


def get_dp825_scenario_data(env, condition):
    db = SqliteConnection()
    db.connect()

    result = db.get_data(table_name="DP825", column_names_and_values={"ENV": "dev11", "condition": condition})

    db.close()

    if result is None:
        raise ValueError(f"No DP825 test data found for ENV={env}, condition={condition}")

    return {"ENV": result[0], "condition": result[1], "client_number": result[2]}


def dp898_payload_setup(condition="valid_client", client_number=None, date_time=None):
    env = os.getenv("API_TEST_ENV", "dev11").strip().lower()

    if env == "d11":
        env = "dev11"

    valid_conditions = {
        "valid_client",
        "no_matching_client",
        "invalid_client_number",
        "missing_client_number",
        "user_not_recognised"
    }

    if condition not in valid_conditions:
        raise ValueError(
            f"Invalid DP898 condition: {condition}. Expected one of: {', '.join(sorted(valid_conditions))}"
        )

    data = get_dp898_scenario_data(env=env, condition=condition).copy()

    if client_number is not None:
        data["client_number"] = str(client_number)

    if condition == "missing_client_number":
        data["client_number"] = None

    username = str(data["username"]).strip()
    transaction_id = pytest.AUTO_TRANSACTION_ID

    return {
        "client_number": data["client_number"],
        "transaction_id": transaction_id,
        "request_date_time": date_time,
        "datapower_headers": payloads.dp898.headers_datapower(username=username),
        "azure_headers": payloads.dp898.headers_azure(username=username),
        "condition": condition,
        "username": username
    }


def get_dp898_scenario_data(env, condition):
    db = SqliteConnection()

    try:
        db.connect()
        result = db.get_data(table_name="DP898", column_names_and_values={"ENV": env, "condition": condition})
    finally:
        db.close()

    if result is None:
        raise ValueError(f"No DP898 test data found for ENV={env}, condition={condition}")

    return {"ENV": result[0], "condition": result[1], "client_number": result[2], "username": result[3]}


def dp901_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("DP901", {"CONDITION": condition})
    db_conn.close()

    headers = payloads.dp901.dp901_headers()
    params = payloads.dp901.dp901_params()

    body = payloads.dp901.dp901_body(
        client_number=data[3],
        action=data[4],
        when_notified=data[5],
        start_date=data[6],
        end_date=data[7],
        income_description=data[8],
        income_type=data[9],
        income_amount=data[10],
        income_frequency=data[11],
        hours_worked=data[12],
        cost_amount=data[13],
        cost_code=data[14],
        cost_frequency=data[15]
    )

    return headers, params, body


def sc550_payload_setup(conditions=None):
    header = payloads.sc550.sc550_headers()
    body = payloads.sc550.sc550_body()

    if conditions == "missing applicant ird":
        del body["applicant"]["IRDNumber"]
    elif conditions == "missing applicant dob":
        del body["applicant"]["dateOfBirth"]
    elif conditions == "missing other carer ref":
        del body["otherCarers"][0]["referenceNumber"]
    elif conditions == "missing trans id":
        del header["transactionid"]
    elif conditions == "invalid applicant ird":
        body["applicant"]["IRDNumber"] = "123456ABC"
    elif conditions == "invalid child ird":
        body["children"][0]["IRDNumber"] = "123456DEF"
    elif conditions == "invalid child ird":
        body["otherCarers"][0]["IRDNumber"] = "123456GHI"
    elif conditions == "invalid applicant ird":
        body["otherCarers"][0]["IRDNumber"] = "131005AAAAAA"
    elif conditions == "invalid child ird":
        body["otherCarers"][0]["IRDNumber"] = "131005BBBBBB"
    elif conditions == "invalid other carer ird":
        body["otherCarers"][0]["IRDNumber"] = "131005CCCCCC"
    elif conditions == "invalid dob":
        body["applicant"]["dateOfBirth"] = "01/01/1981"
    elif conditions == "invalid trans id":
        header["transactionid"] = "hello_world"
    elif conditions == "invalid bank account":  # uses O's instead of zeros
        body["bankAccount"]["account"] = "OO572952"
    elif conditions == "invalid given name":  # max character limit is 256
        body["applicant"]["givenNames"] = "A" * 257

    json_body = json.dumps(body)
    return header, json_body


def sc551_payload_setup(ird_num: str, client_id: str, conditions=None, date_time: str = ""):
    if conditions == "invalid ird number":
        ird_num = "000000000"
    elif conditions == "missing ird number":
        ird_num = "142733404"
        client_id = "526280596"
    elif conditions == "inactive liable parent account":
        ird_num = "139628047"
        client_id = "021215905"

    body = payloads.sc551.sc551_body(ird_num=ird_num, client_id=client_id, formatted_datetime=date_time)
    header = payloads.sc551.sc551_headers()
    if conditions == "invalid start month":
        body = replace_tag_value(body, tag_to_replace="start", replacement_value="2024-03-01")
        body = replace_tag_value(body, tag_to_replace="end", replacement_value="2023-07-01")
    elif conditions == "invalid date range":
        body = replace_tag_value(body, tag_to_replace="end", replacement_value="2025-07-01")
    elif conditions == "invalid start date":
        body = replace_tag_value(body, tag_to_replace="start", replacement_value="2023-06-30")
    elif conditions == "invalid date format":
        body = replace_tag_value(body, tag_to_replace="end", replacement_value=" ")

    return header, body


def sc826_payload_setup(
    payload_type: str,
    conditions: str = None,
    new_headers: dict = None,
    azure: bool = False,
    bulk_test: bool = False,
    bulk_swn: str = ""
):
    body = payloads.sc826.sc826_get_body(payload_type)
    headers = payloads.sc826.sc826_headers()
    if conditions == "secured_client":
        db_conn = SqliteConnection()
        db_conn.connect()
        if not bulk_test:
            client_data = db_conn.get_data("SC826", {"ENV": ENVIRONMENT, "Condition": conditions})
        else:
            client_data = bulk_swn
        db_conn.close()
        if not bulk_test:
            first, middle, last = client_data[2].split()
        else:
            first, middle, last = ("SCEightTwoSix", "secure", "client")
        if payload_type == "all_but_ird":
            body = replace_tag_value(body, tag_to_replace="firstName", replacement_value=first)
            body = replace_tag_value(body, tag_to_replace="middleNames", replacement_value=middle)
            body = replace_tag_value(body, tag_to_replace="familyName", replacement_value=last)
            body = replace_tag_value(body, tag_to_replace="dateOfBirth", replacement_value=client_data[3])
            body = replace_tag_value(body, tag_to_replace="code", replacement_value=client_data[4])
        elif payload_type == "dob_only":
            body = replace_tag_value(body, tag_to_replace="familyName", replacement_value=last)
            body = replace_tag_value(body, tag_to_replace="dateOfBirth", replacement_value=client_data[3])
        elif payload_type == "full_name":
            body = replace_tag_value(body, tag_to_replace="firstName", replacement_value=first)
            body = replace_tag_value(body, tag_to_replace="middleNames", replacement_value=middle)
            body = replace_tag_value(body, tag_to_replace="familyName", replacement_value=last)
        elif payload_type == "ird_only":
            body = replace_tag_value(body, tag_to_replace="identifier", replacement_value=client_data[5])
        elif payload_type == "name_gender":
            body = replace_tag_value(body, tag_to_replace="familyName", replacement_value=last)
            body = replace_tag_value(body, tag_to_replace="code", replacement_value=client_data[4])
    elif conditions == "invalid_user":
        body = replace_tag_value(body, tag_to_replace="id", replacement_value="Bob")
    elif conditions == "invalid_gender":
        body = replace_tag_value(body, tag_to_replace="code", replacement_value="WOMEN")
    elif conditions == "invalid_ird":
        body = replace_tag_value(body, tag_to_replace="code", replacement_value=" ")
    elif conditions == "invalid_name":
        body = replace_tag_value(body, tag_to_replace="firstName", replacement_value="")
        body = replace_tag_value(body, tag_to_replace="middleNames", replacement_value="")
        body = replace_tag_value(body, tag_to_replace="familyName", replacement_value="")
    elif conditions == "50+Clients":
        db_conn = SqliteConnection()
        db_conn.connect()
        client_data = db_conn.get_data("SC826", {"ENV": ENVIRONMENT, "Condition": conditions})
        db_conn.close()
        first, middle, last = client_data[2].split()
        if payload_type == "all_but_ird":
            body = replace_tag_value(body, tag_to_replace="firstName", replacement_value=first)
            body = replace_tag_value(body, tag_to_replace="middleNames", replacement_value=middle)
            body = replace_tag_value(body, tag_to_replace="familyName", replacement_value=last)
            body = replace_tag_value(body, tag_to_replace="dateOfBirth", replacement_value=client_data[3])
            body = replace_tag_value(body, tag_to_replace="code", replacement_value=client_data[4])
        elif payload_type == "full_name":
            body = replace_tag_value(body, tag_to_replace="firstName", replacement_value=first)
            body = replace_tag_value(body, tag_to_replace="middleNames", replacement_value=middle)
            body = replace_tag_value(body, tag_to_replace="familyName", replacement_value=last)
        elif payload_type == "name_gender":
            body = replace_tag_value(body, tag_to_replace="familyName", replacement_value=last)
            body = replace_tag_value(body, tag_to_replace="code", replacement_value=client_data[4])

    tz = timezone(timedelta(hours=12))
    formatted_datetime = datetime.now(tz).isoformat(timespec="seconds")
    transaction_id = f"SC826_AutoTest_{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    body = replace_tag_value(body, tag_to_replace="auditId", replacement_value="AutomationTest")
    body = replace_tag_value(body, tag_to_replace="requestDateTime", replacement_value=formatted_datetime)
    body = replace_tag_value(body, tag_to_replace="transactionId", replacement_value=transaction_id)

    return headers, body


def sc246_payload_setup(conditions: str = None, bulk_test: bool = False, bulk_swn: str = "", date_time: str = ""):
    db_conn = SqliteConnection()
    db_conn.connect()
    if conditions in ["no_identity_verification", "no_matching_client", "invalid_client_number"]:
        client_data = db_conn.get_data(
            table_name="sc246", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": conditions}
        )
    else:
        client_data = db_conn.get_data(
            table_name="sc246", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "None"}
        )
    db_conn.close()

    if not bulk_test:
        body = payloads.sc246.sc246_body(client_data[1], date_time)
    else:
        body = payloads.sc246.sc246_body(bulk_swn, date_time)
    headers = payloads.sc246.sc246_headers()

    if conditions == "user_not_recognised":
        body = replace_tag_value(body, tag_to_replace="id", replacement_value="tbau00005")
    elif conditions == "invalid_sourcesystem":
        body = replace_tag_value(body, tag_to_replace="sourceSystem", replacement_value="BOB")
    elif conditions == "invalid_transactionid":
        body = replace_tag_value(body, tag_to_replace="transactionId", replacement_value="")
    elif conditions == "invalid_securitytoken":
        body = replace_tag_value(body, tag_to_replace="id", replacement_value="")
    elif conditions == "invalid_requestdatetime":
        pass  # Schema checks if the value is a valid value for the "dateTime" datatype so might not be able to test?
        # body = replace_tag_value(body, tag_to_replace="requestDateTime", replacement_value="")

    return headers, body


def dp246_payload_setup(conditions: str = None, bulk_test: bool = False, bulk_swn: str = "", date_time: str = ""):
    db_conn = SqliteConnection()
    db_conn.connect()
    if conditions in ["no_identity_verification", "no_matching_client", "invalid_client_number"]:
        client_data = db_conn.get_data(
            table_name="sc246", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": conditions}
        )
    else:
        client_data = db_conn.get_data(
            table_name="sc246", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "None"}
        )
    db_conn.close()

    if not bulk_test:
        params = payloads.dp246.dp246_params(client_data[1])
    else:
        params = payloads.dp246.dp246_params(bulk_swn)

    headers = payloads.dp246.dp246_headers()

    if conditions == "user_not_recognised":
        headers = payloads.dp247.dp247_headers(user_string="bob:password")
    elif conditions == "invalid_transactionid":
        del params["transactionId"]

    return headers, params


def sc871_payload_setup(condition=None, bulk_test: bool = False, bulk_swn: str = ""):
    env = os.getenv("API_TEST_ENV", "u11")

    if condition not in payloads.sc871.SC871_TEST_DATA.get(env, {}):
        raise ValueError(f"Invalid SC871 condition: {condition}")

    scenario_data = payloads.sc871.SC871_TEST_DATA[env][condition].copy()

    db_conn = SqliteConnection()
    db_conn.connect()

    data = db_conn.get_data("SC871", {"CONDITION": condition})

    db_conn.close()

    if not data:
        raise Exception(f"No SC871 data found in SQLite for condition: {condition}")

    if not bulk_test:
        scenario_data["client_id"] = str(data[1]).strip()
    else:
        scenario_data["client_id"] = bulk_swn
    scenario_data["user_id"] = str(data[2]).strip()

    if not scenario_data.get("client_id"):
        raise Exception(f"SC871 client_id missing for condition: {condition}")

    if not scenario_data.get("user_id"):
        raise Exception(f"SC871 user_id missing for condition: {condition}")

    audit_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")
    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = payloads.sc871.get_payload_sc871(
        audit_id=audit_id, request_date_time=request_date_time, scenario_data=scenario_data
    )

    header = {"Content-Type": "application/xml", "MSD-Sub-Env": env}

    return {"request_body": body, "header": header, "scenario_data": scenario_data}


def sc875_payload_setup(condition=None, bulk_test=False, bulk_swn=""):
    env = os.getenv("API_TEST_ENV", "u11")

    if condition not in payloads.sc875.SC875_TEST_DATA.get(env, {}):
        raise ValueError(f"Invalid SC875 condition: {condition}")

    scenario_data = payloads.sc875.SC875_TEST_DATA[env][condition].copy()

    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("SC875", {"CONDITION": condition})
    db_conn.close()

    if not data:
        raise Exception(f"No SC875 data found in SQLite for condition: {condition}")

    if not bulk_test:
        scenario_data["client_id"] = str(data[1]).strip()
    else:
        scenario_data["client_id"] = bulk_swn
    scenario_data["env"] = env
    scenario_data["user_id"] = scenario_data.get("user_id", "bpmuser")

    audit_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")
    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = payloads.sc875.get_payload_sc875(
        audit_id=audit_id, request_date_time=request_date_time, scenario_data=scenario_data
    )

    header = {"Content-Type": "application/xml", "MSD-Sub-Env": scenario_data["env"]}

    return {"request_body": body, "header": header, "scenario_data": scenario_data}


def sc811_v2_payload_setup(condition=None, bulk_test=False, bulk_swn=""):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(
            table_name="SC811", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC811 data found for ENVIRONMENT={ENVIRONMENT}, CONDITION={condition}")

    if not bulk_test:
        scenario_data = {
            "env": str(data[0]).strip(),
            "condition": str(data[1]).strip(),
            "client_id": str(data[2]).strip(),
            "user_id": str(data[3]).strip()
        }
    else:
        scenario_data = {
            "env": str(data[0]).strip(),
            "condition": str(data[1]).strip(),
            "client_id": bulk_swn,
            "user_id": str(data[3]).strip()
        }

    audit_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")

    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = get_payload_sc811_v2(audit_id=audit_id, request_date_time=request_date_time, scenario_data=scenario_data)

    header = {"Content-Type": "application/xml", "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")}

    return {"request_body": body, "header": header, "scenario_data": scenario_data}


def sc811_v1_payload_setup(condition=None, bulk_test=False, bulk_swn=""):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(
            table_name="SC811", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC811 test data found for ENVIRONMENT={ENVIRONMENT}, CONDITION={condition}")

    scenario_data = {
        "env": str(data[0]).strip(),
        "condition": str(data[1]).strip(),
        "client_id": bulk_swn if bulk_test else str(data[2]).strip(),
        "user_id": str(data[3]).strip()
    }

    audit_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")

    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    body = get_payload_sc811_v1(audit_id=audit_id, request_date_time=request_date_time, scenario_data=scenario_data)

    header = {"Content-Type": "application/xml", "MSD-Sub-Env": os.getenv("API_TEST_ENV", "d11")}

    return {"request_body": body, "header": header, "scenario_data": scenario_data}


def sc901_payload_setup(condition="successful_new_income_declaration"):
    db = SqliteConnection()
    db.connect()

    try:
        sc901_data = db.get_data(
            table_name="SC901", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc901_data:
        raise ValueError(f"No SC901 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc901.get_payload_sc901(
            client_number=sc901_data[3],
            action=sc901_data[4],
            income_type_code=sc901_data[5],
            effective_start_date=sc901_data[6],
            effective_end_date=sc901_data[7]
        ),
        "header": payloads.sc901.get_headers_sc901()
    }


def sc932_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC932", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC932 test data was found in SQLite for condition: {condition}")

    invalid_auth = condition == "authentication_failure"

    return {
        "request_body": payloads.sc932.get_payload_sc932(
            campaign_name=scenario_data[5],
            reference_id=scenario_data[6],
            outcome_id=scenario_data[7],
            outcome_name=scenario_data[8],
            status=scenario_data[9],
            priority=scenario_data[10],
            skill_level=scenario_data[11]
        ),
        "header": payloads.sc932.get_headers_sc932(invalid_auth=invalid_auth),
        "calling_list": scenario_data[3],
        "client_id": scenario_data[4],
        "raise_error": False if condition in ["invalid_request", "authentication_failure"] else True
    }


def sc933_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC933", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC933 test data was found in SQLite for condition: {condition}")

    campaign_name = scenario_data[3]
    operation = scenario_data[4]
    dial_mode = scenario_data[5] or None
    optimize_by = scenario_data[6] or None
    optimize_goal = int(scenario_data[7]) if scenario_data[7] else None
    invalid_auth = condition == "authentication_failure"

    return {
        "campaign_name": campaign_name,
        "start_request_body": payloads.sc933.get_payload_sc933(
            operation="start", dial_mode=dial_mode, optimize_by=optimize_by, optimize_goal=optimize_goal
        ),
        "start_header": payloads.sc933.get_headers_sc933(),
        "stop_request_body": payloads.sc933.get_payload_sc933(operation="stop"),
        "stop_header": payloads.sc933.get_headers_sc933(),
        "reset_header": payloads.sc933.get_headers_sc933(),
        "request_body": payloads.sc933.get_payload_sc933(
            operation=operation, dial_mode=dial_mode, optimize_by=optimize_by, optimize_goal=optimize_goal
        ),
        "header": payloads.sc933.get_headers_sc933(invalid_auth=invalid_auth),
        "operation": operation,
        "raise_error": False
        if condition in ["invalid_request", "campaign_already_stopped", "authentication_failure"]
        else True
    }


def sc247_payload_setup(conditions: str = None, bulk_test: bool = False, bulk_swn: str = ""):
    db_conn = SqliteConnection()
    db_conn.connect()
    if conditions in ["no_matching_client", "invalid_client_number"]:
        client_data = db_conn.get_data(
            table_name="sc247", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": conditions}
        )
    else:
        client_data = db_conn.get_data(
            table_name="sc247", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "None"}
        )
    db_conn.close()

    body = payloads.sc247.sc247_body()
    headers = payloads.sc247.sc247_headers()
    if not bulk_test:
        body = replace_tag_value(body, tag_to_replace="identifier", replacement_value=client_data[1])
    else:
        body = replace_tag_value(body, tag_to_replace="identifier", replacement_value=bulk_swn)

    if conditions == "user_not_recognised":
        body = replace_tag_value(body, tag_to_replace="id", replacement_value="tbau00005")
    elif conditions == "invalid_sourcesystem":
        body = replace_tag_value(body, tag_to_replace="sourceSystem", replacement_value="CMS")
    elif conditions == "invalid_transactionid":
        body = replace_tag_value(body, tag_to_replace="transactionId", replacement_value="")
    elif conditions == "invalid_securitytoken":
        body = replace_tag_value(body, tag_to_replace="id", replacement_value="")
    elif conditions == "invalid_system":
        body = replace_tag_value(body, tag_to_replace="system", replacement_value="CIA")
    elif conditions == "invalid_documenttypecode":
        body = replace_tag_value(body, tag_to_replace="code", replacement_value="XXXX", parent_tag="documentType")
        body = replace_tag_value(
            body, tag_to_replace="description", replacement_value="DOCX", parent_tag="documentType"
        )
    elif conditions == "invalid_dateOfBirthStatus":
        body = replace_tag_value(body, tag_to_replace="dateOfBirth", replacement_value="bob", parent_tag="consistency")
    elif conditions == "invalid_firstNameStatus":
        body = replace_tag_value(body, tag_to_replace="firstName", replacement_value="bob", parent_tag="consistency")
    elif conditions == "invalid_familyNameStatus":
        body = replace_tag_value(body, tag_to_replace="familyName", replacement_value="bob", parent_tag="consistency")
    elif conditions == "invalid_docStatus":
        body = replace_tag_value(body, tag_to_replace="documentPhotoFacialRecognition", replacement_value="bob")
    elif conditions == "invalid_livenesspassstatus":
        body = replace_tag_value(body, tag_to_replace="isSelfieClearAndLive", replacement_value="bob")
    elif conditions == "invalid_datetime":
        body = replace_tag(body, tag_to_replace="ns3:requestDateTime")

    return body, headers


def dp247_payload_setup(conditions: str = None, bulk_test: bool = False, bulk_swn: str = ""):
    db_conn = SqliteConnection()
    db_conn.connect()
    if conditions in ["no_matching_client", "invalid_client_number"]:
        client_data = db_conn.get_data(
            table_name="sc247", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": conditions}
        )
    else:
        client_data = db_conn.get_data(
            table_name="sc247", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "None"}
        )
    db_conn.close()

    body = payloads.dp247.dp247_body()
    headers = payloads.dp247.dp247_headers()
    params = payloads.dp247.dp247_params()
    if not bulk_test:
        body = body.replace("SWN", client_data[1])
    else:
        body = body.replace("SWN", bulk_swn)

    if conditions == "user_not_recognised":
        headers = payloads.dp247.dp247_headers(user_string="bob:password")
    elif conditions == "invalid_transactionid":
        params = ""
    elif conditions == "invalid_system":
        body = body.replace("DIA", "BOB")
    elif conditions == "invalid_documenttypecode":
        body = body.replace("NZPASSPORT", "XXXX")
        body = body.replace("NZ Passport", "DOCX")
    elif conditions == "invalid_dateOfBirthStatus":
        body = re.sub(r'"dateOfBirth"\s*:\s*"Consistent"', '"dateOfBirth" : "bob"', body)
    elif conditions == "invalid_firstNameStatus":
        body = re.sub(r'"firstName"\s*:\s*"Consistent"', '"firstName" : "bob"', body)
    elif conditions == "invalid_familyNameStatus":
        body = re.sub(r'"familyName"\s*:\s*"Consistent"', '"familyName" : "bob"', body)
    elif conditions == "invalid_docStatus":
        body = re.sub(
            r'"documentPhotoFacialRecognition"\s*:\s*"Consistent"', '"documentPhotoFacialRecognition" : "bob"', body
        )
    elif conditions == "invalid_livenesspassstatus":
        body = body.replace("MSDYES", "BOB")
    body = json.loads(body)
    return body, headers, params


def sc824_payload_setup(conditions: str = None, bulk_test: bool = False, bulk_swn: str = ""):
    db_conn = SqliteConnection()
    db_conn.connect()
    client_data = db_conn.get_data(
        table_name="sc824", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": str(conditions)}
    )
    db_conn.close()

    headers = payloads.sc824.sc824_headers()
    body = payloads.sc824.get_payload_sc824()
    if not bulk_test:
        body = replace_tag_value(body, tag_to_replace="identifier", replacement_value=client_data[1])
    else:
        body = replace_tag_value(body, tag_to_replace="identifier", replacement_value=bulk_swn)
    return body, headers, client_data[2]


def sc157_payload_setup(conditions: str = None, azure: bool = False, bulk_test: bool = False, bulk_swn: str = ""):
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        if conditions in ["invalid_swn", "no_js_service", "client_not_recognised"]:
            client_data = db_conn.get_data(
                table_name="sc157", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": str(conditions)}
            )
        else:
            client_data = db_conn.get_data(
                table_name="sc157", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "None"}
            )
        db_conn.close()
        if not bulk_test:
            params = payloads.sc157.sc157_params(client_data[1])
        else:
            params = payloads.sc157.sc157_params(bulk_swn)
    except:
        raise Exception("not able to find correct client for negative scenario, upload on to the SQLite DB")

    headers = payloads.sc157.sc157_headers()
    if azure:
        headers["msd-sub-env"] = ENVIRONMENT.replace("ev", "").replace("at", "")
    if conditions == "no_source_system":
        del headers["sourceSystem"]
    elif conditions == "invalid_user_code":
        headers["securityTokenId"] = "BOB"
    elif conditions == "alpha_numeric_client_number":
        params = payloads.sc157.sc157_params("0000000O0")

    return params, headers


def sc899_payload_setup(conditions: str = None, bulk_test: bool = False, bulk_swn: str = ""):
    db_conn = SqliteConnection()
    db_conn.connect()
    if str(conditions) != "user_not_recognised":
        client_data = db_conn.get_data(
            table_name="sc899", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": str(conditions)}
        )
    else:
        client_data = db_conn.get_data(
            table_name="sc899", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "None"}
        )
    headers = payloads.sc899.sc899_headers()
    if not bulk_test:
        body = payloads.sc899.sc899_body(client_data[1])
    else:
        body = payloads.sc899.sc899_body(bulk_swn)
    if str(conditions) == "user_not_recognised":
        body = replace_tag_value(body, tag_to_replace="id", replacement_value="BOB")

    return body, headers


def dp811_payload_setup(condition=None):
    env = os.getenv("API_TEST_ENV") or os.getenv("Environment") or ENVIRONMENT
    db_env = f"dev{env[1:]}" if env.startswith("d") else env

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC811", {"ENVIRONMENT": db_env, "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No DP811 test data found for environment: {db_env}, condition: {condition}")

    client_number = str(data[2]).strip()

    if condition == "no_matching_record":
        start_date = "1900-01-01"
        end_date = "1901-03-21"
    elif condition == "invalid_request":
        start_date = "2030-01-01"
        end_date = "2010-03-21"
    else:
        start_date = "2010-01-01"
        end_date = "2030-03-21"

    params = payloads.dp811.get_payload_dp811(
        transaction_id=pytest.AUTO_TRANSACTION_ID, client_number=client_number, start_date=start_date, end_date=end_date
    )

    headers = payloads.dp811.get_headers_dp811()
    headers["MSD-Sub-Env"] = env

    return {"params": params, "header": headers, "condition": condition}


def dp871_payload_setup(condition=None, bulk_test: bool = False, bulk_swn: str = ""):
    client_conditions = {
        "update_communication_method_only",
        "invalid_request",
        "client_not_recognised",
        "duplicate_or_fraud_client",
        "duplicate_contact_type",
        "incomplete_client_record"
    }

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        if condition in client_conditions:
            data = db_conn.get_data("SC871", {"CONDITION": condition})
        else:
            data = db_conn.get_data("SC871", {"CONDITION": None})
    finally:
        db_conn.close()

    if data is None:
        raise Exception("DP871 payload setup failed, no suitable data found in local db")

    if not bulk_test:
        client_id = data[1]
    else:
        client_id = bulk_swn

    headers = payloads.dp871.get_headers_dp871()

    headers["MSD-a2c-bypass"] = "true"
    headers["MSD-Sub-Env"] = os.getenv("API_TEST_ENV", "d11")

    request_body = payloads.dp871.get_payload_dp871(client_number=client_id, condition=condition)

    return {"header": headers, "params": {"transactionId": pytest.AUTO_TRANSACTION_ID}, "request_body": request_body}


def sc804_payload_setup(payload_type="v1", client_type="JS_CURRENT", condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()

    if condition == "no_matching_record":
        data = db_conn.get_data("SC804", {"ENV": ENVIRONMENT, "CONDITION": "NO_SERVICES"})
    else:
        data = db_conn.get_data("SC804", {"ENV": ENVIRONMENT, "CONDITION": client_type})
    db_conn.close()
    if data is None:
        raise Exception("SC804 payload setup failed, no suitable data found in local db")

    client_id = data[1]
    headers = payloads.sc804.sc804v1_headers()
    body = payloads.sc804.sc804_get_body(payload_type)
    body = replace_tag_value(body, tag_to_replace="transactionId", replacement_value=pytest.AUTO_TRANSACTION_ID)
    if condition == "client_not_recognised":
        body = replace_tag_value(body, tag_to_replace="clientNumber", replacement_value="000000000")
    else:
        body = replace_tag_value(body, tag_to_replace="clientNumber", replacement_value=client_id)

    if condition == "invalid_request":
        body = replace_tag_value(body, tag_to_replace="end", replacement_value="0066-06-11")
    if client_type == "INACTIVE_SERVICES":
        if payload_type == "v2":
            body = replace_tag_value(body, tag_to_replace="start", replacement_value="1992-07-14+12:00")
            body = replace_tag_value(body, tag_to_replace="includeLatestInactiveAssistance", replacement_value="true")
        else:
            body = replace_tag_value(body, tag_to_replace="start", replacement_value="1992-07-14")

    return headers, body


def sc849_payload_setup(condition: str):
    db_conn = SqliteConnection()
    db_conn.connect()
    if condition in ["activity_type_not_mapped", "no_client_swn"]:
        data = db_conn.get_data("SC849", {"ENV": ENVIRONMENT, "CONDITION": "no_current_activities"})
    else:
        data = db_conn.get_data("SC849", {"ENV": ENVIRONMENT, "CONDITION": condition})
    db_conn.close()
    if data is None:
        raise Exception("SC849 payload setup failed, no suitable data found in local db")

    headers = payloads.sc849.sc849_headers()
    body = payloads.sc849.sc849_get_body()

    tz = timezone(timedelta(hours=12))
    now = datetime.now(tz)
    formatted_datetime = now.isoformat()

    if condition == "no_client_swn":
        body = replace_tag_value(body, tag_to_replace="identifier", replacement_value="")
    else:
        body = replace_tag_value(body, tag_to_replace="identifier", replacement_value=data[1])
    body = replace_tag_value(body, tag_to_replace="transactionId", replacement_value=pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, tag_to_replace="requestDateTime", replacement_value=str(formatted_datetime))
    if condition == "activity_type_not_mapped":
        body = replace_tag_value(body, tag_to_replace="activityType", replacement_value="CALLBACKS")
    if condition == "one_or_more_current_activities":
        body = replace_tag(body, tag_to_replace="ns4:processActivities", replacement_value="")

    return headers, body


def dp806_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("DP806", {"CONDITION": condition})
    db_conn.close()

    headers = payloads.dp806.dp806_headers()

    params = payloads.dp806.dp806_params(
        client_number=data[3],
        repayment_start_date=data[4],
        repayment_end_date=data[5],
        include_active_only=data[6],
        include_heritage_debt=data[7],
        include_rates=data[8],
        include_recoverable_repayments=data[9]
    )

    return headers, params


def dp849_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    if condition == "invalid_activity_code":
        data = db_conn.get_data("sc849", {"ENV": ENVIRONMENT, "CONDITION": "no_current_activities"})
    else:
        data = db_conn.get_data("sc849", {"ENV": ENVIRONMENT, "CONDITION": condition})
    db_conn.close()

    headers = payloads.dp849.dp849_headers()
    params = payloads.dp849.dp849_params()
    body = payloads.dp849.dp849_body()
    body = body.replace("SWN", data[1])

    if condition == "invalid_activity_code":
        body = body.replace("CALLBACK", "BOB")

    body = json.loads(body)
    if condition == "one_or_more_current_activities":
        body["filter"].pop("processActivities", None)

    return headers, params, body


def dp762_payload_setup(conditions=None):
    headers = payloads.dp762.dp762_headers()
    params = payloads.dp762.dp762_params()

    if conditions == "service_locations_found_by_city_only":
        params["suburb"] = "Warkworth"
    elif conditions == "no_service_locations_found":
        params["suburb"] = "Chatham Island"
        params["city"] = "Chatham Island"

    return headers, params


def dp804_payload_setup(client_type="JS_CURRENT", condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    if condition == "no_matching_record":
        data = db_conn.get_data("SC804", {"ENV": ENVIRONMENT, "CONDITION": "NO_SERVICES"})
    else:
        data = db_conn.get_data("SC804", {"ENV": ENVIRONMENT, "CONDITION": client_type})
    db_conn.close()
    if data is None:
        raise Exception("DP804 payload setup failed, no suitable data found in local db")

    headers = payloads.dp804.dp804_headers()
    if condition == "client_not_recognised":
        params = payloads.dp804.dp804_params("000000001")
    else:
        params = payloads.dp804.dp804_params(data[1])

    if condition == "invalid_request":
        del params["activePeriodEnd"]

    return headers, params


def dp873_payload_setup(condition: str):
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(
            table_name="SC873", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC873 test data was found in SQLite for DP873 condition: {condition}")

    headers = payloads.dp873.dp873_headers()
    if condition == "invalid_client_number":
        params = payloads.dp873.dp873_params(
            client_swn="000000000", start_date=str(data[4]), end_date=str(data[5]), include_partner=data[6]
        )
    else:
        params = payloads.dp873.dp873_params(
            client_swn=str(data[3]), start_date=str(data[4]), end_date=str(data[5]), include_partner=data[6]
        )
    return headers, params


def sc876_payload_setup(condition=None):
    supported_conditions = {"successful_transaction", "invalid_message", "unrecognised_cnp_id", "swiftt_user_not_found"}

    if condition not in supported_conditions:
        condition = "successful_transaction"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC876", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"SC876 payload setup failed, no test data found for condition: {condition}")

    # Expected SQLite column order:
    # 0 = CONDITION
    # 1 = CLIENT_ID
    # 2 = USER_ID

    client_id = data[1]
    user_id = data[2]

    audit_id = str(uuid4())
    correlation_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")

    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    source_system = "BPM"

    if condition == "invalid_message":
        source_system = "TEST"

    body = payloads.sc876.get_payload_sc876(
        audit_id=audit_id,
        correlation_id=correlation_id,
        request_date_time=request_date_time,
        client_id=client_id,
        user_id=user_id,
        source_system=source_system
    )

    header = payloads.sc876.get_headers_sc876()

    return {"request_body": body, "header": header, "client_id": client_id, "user_id": user_id, "condition": condition}


def sc1001_v1_payload_setup(condition=None):
    supported_conditions = {
        "valid_supergold_card",
        "no_supergold_card",
        "incorrect_date_of_birth",
        "invalid_client_number",
        "invalid_date_of_birth"
    }

    if condition not in supported_conditions:
        condition = "valid_supergold_card"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC1001", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"SC1001 payload setup failed, no test data found for condition: {condition}")

    # Expected SQLite column order:
    # 0 = CONDITION
    # 1 = CLIENT_NUMBER
    # 2 = DATE_OF_BIRTH

    client_number = str(data[1]).strip()
    date_of_birth = str(data[2]).strip()

    audit_id = str(uuid4())

    requested_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")

    requested_date_time = requested_date_time[:-2] + ":" + requested_date_time[-2:]

    request_body = payloads.sc1001_v1.get_payload_sc1001(
        client_number=client_number,
        date_of_birth=date_of_birth,
        audit_id=audit_id,
        transaction_id=pytest.AUTO_TRANSACTION_ID,
        requested_date_time=requested_date_time
    )

    header = payloads.sc1001_v1.get_headers_sc1001()

    return {
        "request_body": request_body,
        "header": header,
        "client_number": client_number,
        "date_of_birth": date_of_birth,
        "audit_id": audit_id,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "requested_date_time": requested_date_time,
        "condition": condition
    }


def sc1001_v2_payload_setup(condition=None):
    supported_conditions = {
        "community_service_card",
        "combo_card",
        "veteran_combo_card",
        "supergold_without_valid_csc",
        "no_csc_card",
        "incorrect_date_of_birth",
        "client_not_found",
        "client_number_with_leading_zeros",
        "invalid_request"
    }

    if condition not in supported_conditions:
        condition = "community_service_card"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC1001_V2", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"SC1001 V2 payload setup failed, no test data found for condition: {condition}")

    # Expected SQLite column order:
    # 0 = CONDITION
    # 1 = CLIENT_NUMBER
    # 2 = DATE_OF_BIRTH
    # 3 = ENV

    client_number = str(data[1]).strip()
    date_of_birth = str(data[2]).strip()

    # Default concession type
    concession_type = "CommunityServices"

    # Invalid request scenario
    if condition == "invalid_request":
        concession_type = "test"

    audit_id = str(uuid4())

    requested_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")

    requested_date_time = requested_date_time[:-2] + ":" + requested_date_time[-2:]

    request_body = payloads.sc1001_v2.get_payload_sc1001_v2(
        client_number=client_number,
        date_of_birth=date_of_birth,
        audit_id=audit_id,
        transaction_id=pytest.AUTO_TRANSACTION_ID,
        requested_date_time=requested_date_time,
        concession_type=concession_type
    )

    header = payloads.sc1001_v2.get_headers_sc1001_v2()

    return {
        "request_body": request_body,
        "header": header,
        "client_number": client_number,
        "date_of_birth": date_of_birth,
        "audit_id": audit_id,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "requested_date_time": requested_date_time,
        "concession_type": concession_type,
        "condition": condition
    }


def sc588_payload_setup(condition=None):
    if condition not in ["successful", "client_not_present"]:
        condition = "successful"

    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "SC588.csv"

    client_number = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row["CONDITION"].strip() == condition:
                client_number = row["CLIENT_NUMBER"].strip()
                break

    if client_number is None:
        raise Exception(f"DP588 payload setup failed, no test data found for condition: {condition}")

    header = payloads.sc588.get_headers_sc588()
    params = payloads.sc588.get_params_sc588(client_number=client_number, transaction_id=pytest.AUTO_TRANSACTION_ID)

    return {
        "header": header,
        "params": params,
        "client_number": client_number,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "condition": condition
    }


def dp588_payload_setup(condition=None):
    supported_conditions = {"successful", "client_not_present"}

    if condition not in supported_conditions:
        condition = "successful"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC588", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"DP588 payload setup failed, no test data found for condition: {condition}")

    client_number = str(data[0]).strip()

    params = payloads.dp588.get_params_dp588(client_number=client_number, transaction_id=pytest.AUTO_TRANSACTION_ID)

    header = payloads.dp588.get_headers_dp588()

    return {
        "header": header,
        "params": params,
        "client_number": client_number,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "condition": condition
    }


def dp850_payload_setup(condition=None):
    if condition != "successful_transaction":
        condition = "successful_transaction"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC850", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"DP850 payload setup failed, no test data found for condition: {condition}")

    client_number = str(data[0]).strip()

    header = payloads.dp850.get_headers_dp850()

    return {
        "request_body": payloads.dp850.get_payload_dp850(client_number=client_number),
        "header": header,
        "params": payloads.dp850.get_params_dp850(transaction_id=pytest.AUTO_TRANSACTION_ID),
        "client_number": client_number,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "condition": condition
    }


def sc850_payload_setup(condition=None):
    supported_conditions = {"successful_transaction"}

    if condition not in supported_conditions:
        condition = "successful_transaction"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC850", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"SC850 payload setup failed, no test data found for condition: {condition}")
    # SC850 SQLite column order:
    # 0 = CLIENT_NUMBER
    # 1 = CONDITION
    # 2 = ENV

    client_number = data[0]

    request_date_time = datetime.now().astimezone().isoformat()

    request_body = payloads.sc850.get_payload_sc850(client_number=client_number, request_date_time=request_date_time)

    return {"request_body": request_body, "header": payloads.sc850.get_headers_sc850(), "params": {}}


def sc555_payload_setup(condition=None):
    supported_conditions = {
        "transactions_found",
        "no_transactions",
        "end_date_before_start_date",
        "unknown_card_number"
    }

    if condition not in supported_conditions:
        condition = "no_transactions"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC555", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"SC555 payload setup failed, no test data found for condition: {condition}")

    # Expected SQLite column order:
    # 0 = CONDITION
    # 1 = CARD_NUMBER
    # 2 = START_DATE
    # 3 = END_DATE

    card_number = str(data[1])
    start_date = str(data[2])
    end_date = str(data[3])

    body = payloads.sc555.get_payload_sc555(card_number=card_number, start_date=start_date, end_date=end_date)

    return {
        "request_body": body,
        "header": payloads.sc555.get_headers_sc555(),
        "card_number": card_number,
        "start_date": start_date,
        "end_date": end_date,
        "condition": condition
    }


def sc812_payload_setup(condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        data = db_conn.get_data("SC812", {"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()
    headers = payloads.sc812.sc812_headers()
    body = payloads.sc812.sc812_body()
    body = replace_tag_value(body, "clientNumber", data[1])
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, "end", "2026-08-10")
    if condition == "decades_old_services":
        body = replace_tag_value(body, "start", "1993-01-01")
    elif condition == "no_matching_record":
        body = replace_tag_value(body, "end", "2026-07-21")
        body = replace_tag_value(body, "start", "2026-07-20")
    else:
        body = replace_tag_value(body, "start", "2026-08-10")
    return headers, body


def dp812_payload_setup(condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        data = db_conn.get_data("SC812", {"ENV": ENVIRONMENT, "CONDITION": "decades_old_services"})
    finally:
        db_conn.close()
    headers = payloads.dp812.dp812_headers()

    if condition == "none":
        params = payloads.dp812.dp812_params(data[1])
    elif condition == "INCOMEABATEMENT":
        params = payloads.dp812.dp812_params(data[1], factor_entitlement="INCOMEABATEMENT")
    elif condition == "SANCTION":
        params = payloads.dp812.dp812_params(data[1], factor_entitlement="SANCTION")
    elif condition == "SECTION70A":
        params = payloads.dp812.dp812_params(data[1], factor_entitlement="SECTION70A")
    elif condition == "TenYearsNZResidencySinceBirth":
        params = payloads.dp812.dp812_params(data[1], factor_entitlement="TenYearsNZResidencySinceBirth")
    elif condition == "includeFullEntitlement_No":
        params = payloads.dp812.dp812_params(data[1], full_entitlement="false")
    elif condition == "includeNotionalRate_No":
        params = payloads.dp812.dp812_params(data[1], notional_rate="false")
    elif condition == "includePaymentRate_No":
        params = payloads.dp812.dp812_params(data[1], payment_rate="false")
    elif condition == "includePortabilityProvision_No":
        params = payloads.dp812.dp812_params(data[1], prot_provision="false")
    elif condition == "includeTaxRate_No":
        params = payloads.dp812.dp812_params(data[1], tax_rate="false")
    elif condition == "client_not_recognised":
        params = payloads.dp812.dp812_params("526323000")
    elif condition == "invalid_request":
        params = payloads.dp812.dp812_params("1234567890")
    elif condition == "no_matching_record":
        params = payloads.dp812.dp812_params(data[1], start_date="2026-08-10")
    else:
        raise Exception("Unknown condition")

    return headers, params


def sc864_payload_setup(condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    conditions = ["food", "dental", "food_and_dental", "user_not_recognised"]
    try:
        if condition in conditions:
            data = db_conn.get_data("SC864", {"ENV": ENVIRONMENT, "CONDITION": None})
        else:
            data = db_conn.get_data("SC864", {"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()
    headers = payloads.sc864.sc864_headers()
    body = payloads.sc864.sc864_body()
    body = replace_tag_value(body, "clientNumber", data[1])
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    if condition == "food":
        body = replace_tag_value(body, "code", "FOOD")
    elif condition == "food_and_dental":
        body = replace_tag_value(body, "code", "FOOD")
        ns = {
            "ns4": "http://msd.govt.nz/integration/derived/entitlement/schema/entitlementmessage/v1",
            "ns5": "http://msd.govt.nz/integration/utils/technical/schema/value/v1"
        }
        root = et.fromstring(body)
        # Find the filter node
        filter_elem = root.find(".//ns4:filter", ns)
        new_need = et.SubElement(
            filter_elem,
            "{http://msd.govt.nz/integration/derived/entitlement/schema/entitlementmessage/v1}hardshipSNGNeed"
        )
        new_code = et.SubElement(new_need, "{http://msd.govt.nz/integration/utils/technical/schema/value/v1}code")
        new_code.text = "DENTAL"
        body = et.tostring(root, encoding="unicode")
    else:
        body = replace_tag_value(body, "code", "DENTAL")

    if condition == "user_not_recognised":
        body = replace_tag_value(body, "id", "bobby")
    if condition == "transaction_unsuccessful":
        body = replace_tag_value(body, "code", "FOODS")

    return headers, body


def dp864_payload_setup(condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        if condition != "no_matching_record":
            data = db_conn.get_data("SC864", {"ENV": ENVIRONMENT, "CONDITION": "None"})
        else:
            data = db_conn.get_data("SC864", {"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()
    headers = payloads.dp864.dp864_headers()
    if condition == "dental":
        params = payloads.dp864.dp864_params(data[1], "DENTAL", "false", "false")
    elif condition == "food":
        params = payloads.dp864.dp864_params(data[1], "FOOD", "false", "false")
    elif condition == "hardship_count":
        params = payloads.dp864.dp864_params(data[1], "None", "true", "false")
        del params["hardshipSNGNeed"]
    elif condition == "advance_balance":
        params = payloads.dp864.dp864_params(data[1], "None", "false", "true")
        del params["hardshipSNGNeed"]
    elif condition == "all" or condition == "no_matching_record":
        params = payloads.dp864.dp864_params(data[1], "FOOD", "true", "true")
    elif condition == "client_not_recognised":
        params = payloads.dp864.dp864_params("100000000", "FOOD", "true", "true")
    elif condition == "transaction_unsuccessful":
        params = payloads.dp864.dp864_params(data[1], "FOODS", "true", "true")
    else:
        raise Exception("Unknown scenario condition")

    return headers, params


def sc557_payload_setup(condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        data = db_conn.get_data("SC557", {"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()
    headers = payloads.sc557.sc557_headers()
    body = payloads.sc557.sc557_body()
    body = body.replace("SWN", data[1])
    body = body.replace("TRANSID", pytest.AUTO_TRANSACTION_ID)
    return headers, body


def sc510_payload_setup(condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        data = db_conn.get_data("SC510", {"ENV": ENVIRONMENT, "CONDITION": condition})
        # if no payment card already assigned to the client find one from mock EGW
        if data[2] == "NONE":
            card_no = get_next_pc_insert_into_db()
            db_conn.update_data("SC510", {"condition": condition}, {"card_no": card_no})
    finally:
        db_conn.close()
    headers = payloads.sc510.sc510_headers()
    body = payloads.sc510.sc510_body()
    body = body.replace("SWN", data[1]).replace("CARDNUMBER", data[2]).replace("TRANSID", pytest.AUTO_TRANSACTION_ID)
    return headers, body


def sc556_payload_setup(condition=None):
    body = payloads.sc556.get_payload_sc556()
    headers = payloads.sc556.get_headers_sc556()
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    if condition == "invalid_end_date":
        body = replace_tag_value(body, "endDate", "2024-01-01T00:00:00")
    return headers, body


def sc560_payload_setup(condition=None):
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        data = db_conn.get_data("SC560", {"ENV": ENVIRONMENT, "CONDITION": "None"})
    finally:
        db_conn.close()
    headers = payloads.sc560.sc560_headers()
    body = payloads.sc560.sc560_body()
    if condition == "card_not_recognised":
        body = (
            body.replace("PAYMENTCARD", "5035137030800000")
            .replace("BLOCK", data[2])
            .replace("VECTOR", data[3])
            .replace("KEY", data[4])
            .replace("TRANSID", pytest.AUTO_TRANSACTION_ID)
        )
    else:
        body = (
            body.replace("PAYMENTCARD", data[1])
            .replace("BLOCK", data[2])
            .replace("VECTOR", data[3])
            .replace("KEY", data[4])
            .replace("TRANSID", pytest.AUTO_TRANSACTION_ID)
        )
    return headers, body


def sc557v2_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc557v2.get_payload_sc557v2(),
        "header": payloads.sc557v2.get_headers_sc557v2(),
        "condition": condition
    }


def sc511_payload_setup(condition=None):
    headers = payloads.sc511.sc511_headers()
    body = payloads.sc511.sc511_body()
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        data = db_conn.get_data("SC511", {"ENV": ENVIRONMENT, "CONDITION": condition})
        # if no payment card already assigned to the client find one from mock EGW
        if data[2] == "NONE":
            card_no = get_next_pc_insert_into_db()
            db_conn.update_data("SC511", {"condition": condition}, {"card_no": card_no})
            data[2] = card_no
    finally:
        db_conn.close()
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, "cardNumber", data[2])
    body = replace_tag_value(body, "clientNumber", data[1])

    return headers, body


def sc535_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc535.get_payload_sc535(),
        "header": payloads.sc535.get_headers_sc535(),
        "condition": condition
    }


def sc539_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc539.get_payload_sc539(),
        "header": payloads.sc539.get_headers_sc539(),
        "condition": condition
    }


def sc540_payload_setup(condition=None):
    supported_conditions = {"successful_response", "invalid_xml", "invalid_total_amount"}

    if condition not in supported_conditions:
        condition = "successful_response"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC540", {"CONDITION": condition})
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"SC540 payload setup failed, no test data found for condition: {condition}")

    # SQLite column order:
    # 0 = CONDITION
    # 1 = SOURCE_PAYMENT_REFERENCE
    # 2 = AMOUNT_SPENT
    # 3 = EXPIRY_NOTIFIED_DATE

    source_payment_reference = str(data[1])
    amount_spent = str(data[2])
    expiry_notified_date = str(data[3])

    body = payloads.sc540.get_payload_sc540(
        source_payment_reference=source_payment_reference,
        amount_spent=amount_spent,
        expiry_notified_date=expiry_notified_date,
        condition=condition
    )

    return {"request_body": body, "header": payloads.sc540.get_headers_sc540(), "condition": condition}


def sc553_payload_setup(condition="successful_transaction"):
    supported_conditions = {"successful_transaction", "superseded_request", "invalid_xml", "invalid_merchant_id"}

    if condition not in supported_conditions:
        condition = "successful_transaction"

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC553", {"CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC553 test data found for condition: {condition}")

    # SQLite column order:
    # 0 = CONDITION
    # 1 = EFTPOS_MERCHANT_ID
    # 2 = MSD_MERCHANT_ID
    # 3 = ENVIRONMENT

    eftpos_merchant_id = data[1]
    msd_merchant_id = data[2]

    request_body = payloads.sc553.get_payload_sc553(
        eftpos_merchant_id=eftpos_merchant_id, msd_merchant_id=msd_merchant_id
    )

    return {"request_body": request_body, "header": payloads.sc553.get_headers_sc553(), "condition": condition}


def dp553_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC553", {"CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC553 test data found for DP553 condition: {condition}")

    # SQLite column order:
    # 0 = CONDITION
    # 1 = EFTPOS_MERCHANT_ID
    # 2 = MSD_MERCHANT_ID
    # 3 = ENVIRONMENT

    eftpos_merchant_id = data[1]
    msd_merchant_id = data[2]

    return {
        "request_body": payloads.dp553.get_payload_dp553(
            eftpos_merchant_id=eftpos_merchant_id, msd_merchant_id=msd_merchant_id
        ),
        "header": payloads.dp553.get_headers_dp553(),
        "condition": condition
    }


def sc886_payload_setup(condition="ongoing_application_found"):
    db = SqliteConnection()
    db.connect()

    try:
        sc886_data = db.get_data(
            table_name="SC886", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc886_data:
        raise ValueError(f"No SC886 test data was found in SQLite for condition: {condition}")

    client_number = sc886_data[3]
    search_start_date = sc886_data[4]
    search_end_date = sc886_data[5]
    user_id = sc886_data[6]

    audit_id = str(uuid.uuid4())
    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    return {
        "request_body": payloads.sc886.get_payload_sc886(
            audit_id=audit_id,
            request_date_time=request_date_time,
            client_number=client_number,
            search_start_date=search_start_date,
            search_end_date=search_end_date,
            security_token_id=user_id,
            condition=condition
        ),
        "header": payloads.sc886.get_headers_sc886(),
        "raise_error": True
    }


def dp886_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("DP886", {"CONDITION": condition})
    db_conn.close()

    headers = payloads.dp886.dp886_headers()
    headers["MSD-Sub-Env"] = "d11"

    params = payloads.dp886.dp886_params(client_number=data[3], search_period_start=data[4], search_period_end=data[5])

    if condition == "missing_client_number":
        params.pop("clientNumber", None)
    elif condition == "missing_search_period_start":
        params.pop("searchPeriodStart", None)
    return headers, params


def sc887_payload_setup(condition="ongoing_application_found"):
    db = SqliteConnection()
    db.connect()

    try:
        sc887_data = db.get_data(
            table_name="SC887", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc887_data:
        raise ValueError(f"No SC887 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc887.get_payload_sc887(case_reference=sc887_data[3], user_id=sc887_data[4]),
        "header": payloads.sc887.get_headers_sc887(),
        "raise_error": True
    }


def dp887_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("DP887", {"CONDITION": condition})
    db_conn.close()

    headers = payloads.dp887.dp887_headers()
    headers["MSD-Sub-Env"] = "d11"

    params = payloads.dp887.dp887_params(
        case_references=data[3],
        include_application_obligation=data[4],
        include_evidence_list=data[5],
        include_partner=data[6],
        include_potential_obligation=data[7],
        include_pre_benefit_activity=data[8],
        include_application_appointment=data[9],
        include_application_verification=data[10],
        include_application_change_type=data[11]
    )

    if condition == "invalid_request":
        params.pop("caseReferences", None)

    return headers, params


def sc878_payload_setup(condition="approved_hardship_application_found"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC878", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC878 test data was found in SQLite for condition: {condition}")

    client_number = scenario_data[3]
    security_token_id = scenario_data[4] or "mymsduser"
    include_client_number = condition != "missing_client_number"

    return {
        "request_body": payloads.sc878.get_payload_sc878(
            client_number=client_number,
            security_token_id=security_token_id,
            include_client_number=include_client_number
        ),
        "header": payloads.sc878.get_headers_sc878(),
        "raise_error": True
    }


def dp878_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("DP878", {"CONDITION": condition})
    db_conn.close()

    headers = payloads.dp878.dp878_headers()
    headers["MSD-Sub-Env"] = "d11"

    params = payloads.dp878.dp878_params(client_number=data[3])

    if condition == "missing_client_number":
        params.pop("clientNumber", None)
    elif condition == "missing_transaction_id":
        params.pop("transactionId", None)

    return headers, params


def sc879_payload_setup(condition="hardship_application_found"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC879", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC879 test data was found in SQLite for condition: {condition}")

    client_number = scenario_data[3]
    security_token_id = scenario_data[4] or "mymsduser"
    include_client_number = condition != "invalid_request"

    return {
        "request_body": payloads.sc879.get_payload_sc879(
            client_number=client_number,
            security_token_id=security_token_id,
            include_client_number=include_client_number
        ),
        "header": payloads.sc879.get_headers_sc879(),
        "raise_error": True
    }


def dp879_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("DP879", {"CONDITION": condition})
    db_conn.close()

    headers = payloads.dp879.dp879_headers()
    headers["MSD-Sub-Env"] = "d11"

    params = payloads.dp879.dp879_params(
        client_number=data[3], search_period_start=data[4], search_period_end=data[5], status=data[6]
    )

    for param in ("searchPeriodStart", "searchPeriodEnd", "status"):
        if not params.get(param):
            params.pop(param, None)

    if condition == "invalid_request":
        params.pop("clientNumber", None)

    return headers, params


def sc892_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc892_data = db.get_data(
            table_name="SC892", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc892_data:
        raise ValueError(f"No SC892 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc892.get_payload_sc892(client_number=sc892_data[3], case_reference=sc892_data[4]),
        "header": payloads.sc892.get_headers_sc892(),
        "raise_error": True
    }


def dp892_payload_setup(condition):
    db_conn = SqliteConnection()
    db_conn.connect()
    data = db_conn.get_data("DP892", {"CONDITION": condition})
    db_conn.close()

    headers = payloads.dp892.dp892_headers()
    headers["MSD-Sub-Env"] = "d11"

    params = payloads.dp892.dp892_params(case_references=data[3], client_number=data[4])

    if condition == "invalid_request":
        params.pop("caseReferences", None)

    return headers, params


def sc882_payload_setup(condition="approval_request_received"):
    db = SqliteConnection()
    db.connect()

    try:
        sc882_data = db.get_data(
            table_name="SC882", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc882_data:
        raise ValueError(f"No SC882 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc882.get_payload_sc882(case_reference=sc882_data[3], user_id=sc882_data[4]),
        "header": payloads.sc882.get_headers_sc882(),
        "raise_error": True
    }


def sc869_payload_setup(condition="successful_food"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC869", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC869 test data was found in SQLite for condition: {condition}")

    client_number = str(scenario_data[3])
    payment_card_number = str(scenario_data[4])
    need_type_code = scenario_data[5] or "N1"
    recipient_type = scenario_data[6] or "SUPPLIER"
    requested_amount = scenario_data[7] or "100"
    security_token_id = scenario_data[8] or "mymsduser"

    return {
        "request_body": payloads.sc869.get_payload_sc869(
            client_number=client_number,
            payment_card_number=payment_card_number,
            need_type_code=need_type_code,
            recipient_type=recipient_type,
            requested_amount=requested_amount,
            security_token_id=security_token_id
        ),
        "header": payloads.sc869.get_headers_sc869(),
        "raise_error": True
    }


def sc881_payload_setup(condition="non_recoverable_special_needs_grant"):
    db = SqliteConnection()
    db.connect()

    try:
        sc881_data = db.get_data(
            table_name="SC881", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc881_data:
        raise ValueError(f"No SC881 test data was found in SQLite for condition: {condition}")

    case_reference = sc881_data[3]
    entitlement_type_code = sc881_data[4]
    entitlement_type_description = sc881_data[5]
    is_recoverable = str(sc881_data[6]).lower() == "true"
    recovery_rate = sc881_data[7]
    amount = sc881_data[8]

    return {
        "request_body": payloads.sc881.get_payload_sc881(
            case_reference=case_reference,
            entitlement_type_code=entitlement_type_code,
            entitlement_type_description=entitlement_type_description,
            is_recoverable=is_recoverable,
            recovery_rate=recovery_rate,
            amount=amount
        ),
        "header": payloads.sc881.get_headers_sc881(),
        "raise_error": True
    }


def sc888_payload_setup(payload_type: str, condition: str = None):
    db = SqliteConnection()
    db.connect()
    try:
        negative_scenarios = [
            "INVALID_CASEREFERENCE",
            "MISSING_CASEREFERENCE",
            "CLIENT_NOT_RECOGNISED",
            "INVALID_SWN",
            "USER_NOT_RECOGNISED"
        ]
        if condition in negative_scenarios:
            if payload_type == "id_verification":
                data = db.get_data(
                    table_name="SC888",
                    column_names_and_values={
                        "ENV": ENVIRONMENT,
                        "payload_type": "id_verification",
                        "CONDITION": "ID_PROVIDED"
                    }
                )
            elif payload_type == "obligations_verification":
                data = db.get_data(
                    table_name="SC888",
                    column_names_and_values={
                        "ENV": ENVIRONMENT,
                        "payload_type": "obligations_verification",
                        "CONDITION": "OBLIGATIONS_ACCEPTED"
                    }
                )
            else:
                raise ValueError(f"Unknown payload_type: {payload_type}")
        else:
            data = db.get_data(table_name="SC888", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()

    headers = payloads.sc888.get_headers_sc888()
    body = payloads.sc888.get_sc888_body(payload_type)
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, "identifier", data[1])
    body = replace_tag_value(body, "caseReference", data[2])
    if payload_type == "id_verification":
        body = replace_tag_value(body, "code", data[4], "identityVerificationAction")
        body = replace_tag_value(body, "description", data[5], "identityVerificationAction")
    elif payload_type == "obligations_verification":
        body = replace_tag_value(body, "code", data[4], "decision")
        body = replace_tag_value(body, "description", data[5], "decision")

    if condition == "INVALID_CASEREFERENCE":
        body = replace_tag_value(body, "caseReference", "90000000")
    elif condition == "MISSING_CASEREFERENCE":
        body = replace_tag_value(body, "caseReference", "")
    elif condition == "CLIENT_NOT_RECOGNISED":
        body = replace_tag_value(body, "identifier", "000000001")
    elif condition == "INVALID_SWN":
        body = replace_tag_value(body, "identifier", f"{data[1]}0")
    elif condition == "USER_NOT_RECOGNISED":
        body = replace_tag_value(body, "id", "bobby")

    return headers, body


def dp888_payload_setup(
    application_consent: str, relationship_confirmation: str, application_verification: str, condition: str
):
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC888", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "ID_PROVIDED"})
    finally:
        db.close()

    headers = payloads.dp888.get_headers_dp888()
    params = payloads.dp888.dp888_params()
    body = payloads.dp888.get_dp888_body()

    if condition == "transaction_unsuccessful":
        body = (
            body.replace("CASEREF", "900472660")
            .replace("SWN", data[1])
            .replace("APPCONSENTCODE", application_consent)
            .replace("RELATIONCONFIRMCODE", relationship_confirmation)
            .replace("IDVERIFICATIONCODE", application_verification)
        )
    elif condition == "invalid_request":
        body = (
            body.replace("CASEREF", "")
            .replace("SWN", data[1])
            .replace("APPCONSENTCODE", application_consent)
            .replace("RELATIONCONFIRMCODE", relationship_confirmation)
            .replace("IDVERIFICATIONCODE", application_verification)
        )
    else:
        body = (
            body.replace("CASEREF", data[2])
            .replace("SWN", data[1])
            .replace("APPCONSENTCODE", application_consent)
            .replace("RELATIONCONFIRMCODE", relationship_confirmation)
            .replace("IDVERIFICATIONCODE", application_verification)
        )

    if application_consent == "ACCEPTED":
        body = body.replace("APPCONSENTDESC", "Client has accepted obligations")
    elif application_consent == "DISCUSS":
        body = body.replace("APPCONSENTDESC", "Client wants to discuss obligations")

    if relationship_confirmation == "ACCEPTED":
        body = body.replace("RELATIONCONFIRMDESC", "Client accepts the relationship status")
    elif relationship_confirmation == "REJECTED":
        body = body.replace("RELATIONCONFIRMDESC", "Client rejects the relationship status")
    elif relationship_confirmation == "NODECISION":
        body = body.replace("RELATIONCONFIRMDESC", "No decision recorded")

    if application_verification == "PROVIDED":
        body = body.replace("IDVERIFICATIONDESC", "Identity client document provided/uploaded")
    elif application_verification == "CANNOTPROVIDE":
        body = body.replace("IDVERIFICATIONDESC", "Identity client document cannot be provided/uploaded")
    elif application_verification == "CANNOTNODOCS":
        body = body.replace("IDVERIFICATIONDESC", "Client does not have ID documents that MSD needs to verify identity")
    elif application_verification == "ACCEPTBRING":
        body = body.replace(
            "IDVERIFICATIONDESC", "Client acknowledged that they need to bring ID documents into MSD service centre"
        )
    body = json.loads(body)
    return headers, params, body


def sc872_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc872.get_payload_sc872(),
        "header": payloads.sc872.get_headers_sc872(),
        "condition": condition
    }


def sc880_payload_setup(condition: str = None):
    headers = payloads.sc880.get_headers_sc880()
    body = payloads.sc880.get_payload_sc880()
    db = SqliteConnection()
    db.connect()
    negative_conditions = ["user_not_recognised", "invalid_request"]
    try:
        if condition in negative_conditions:
            data = db.get_data(
                table_name="SC880", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
            )
        else:
            data = db.get_data(table_name="SC880", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()

    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, "caseReference", data[1])
    if condition == "user_not_recognised":
        body = replace_tag_value(body, "id", "bobby")
    elif condition == "invalid_request":
        body = replace_tag(body, "ns6:paymentCardNumber", "")
    return headers, body


def sc821_payload_setup(condition: str = None):
    headers = payloads.sc821.get_headers_sc821()
    body = payloads.sc821.get_payload_sc821()
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC821", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, "clientNumber", data[1])

    return headers, body


def sc820_payload_setup(condition: str):
    headers = payloads.sc820.get_headers_sc820()
    body = payloads.sc820.sc804_get_body(condition=condition)
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC820", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()

    body = replace_tag_value(body, "client", data[1])
    if condition == "transaction_unsuccessful":
        body = replace_tag_value(body, "clientNumber", data[1])

    return headers, body


def sc250_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc250.get_payload_sc250(),
        "header": payloads.sc250.get_headers_sc250(),
        "condition": condition
    }


def sc582_payload_setup():
    headers = payloads.sc582.get_headers_sc582()
    body = payloads.sc582.get_payload_sc582()

    return headers, body


def sc583_payload_setup():
    headers = payloads.sc583.get_headers_sc583()
    body = payloads.sc583.get_payload_sc583()

    return headers, body


def sc867_payload_setup(condition):
    headers = payloads.sc867.get_headers_sc867()
    body = payloads.sc867.get_payload_sc867()
    iib_body, azure_body = None, None
    db = SqliteConnection()
    db.connect()
    try:
        if condition == "user_not_recognised":
            data = db.get_data(
                table_name="SC867", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
            )
        else:
            data = db.get_data(table_name="SC867", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()
    names = data[2].split()
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, "clientNumber", data[1])
    body = replace_tag_value(body, "dateOfBirth", data[3])
    body = replace_tag_value(body, "firstName", names[0])
    body = replace_tag_value(body, "middleNames", names[1])
    body = replace_tag_value(body, "familyName", names[2])
    if data[4] == "None":
        """Generate a random number for the medical certificate ID, the same ID cannot be used mutiple times"""
        # Randomly pick a digit length between 1 and 27
        length = random.randint(1, 27)
        # Determine the lower and upper bounds for that exact length
        lower_bound = 10 ** (length - 1)
        upper_bound = (10**length) - 1
        # Generate the random number within those boundaries
        random_number_iib = random.randint(lower_bound, upper_bound)
        random_number_azure = random.randint(lower_bound, upper_bound)
        iib_body = replace_tag_value(body, "identifier", f"MSD-{random_number_iib}")
        azure_body = replace_tag_value(body, "identifier", f"MSD-{random_number_azure}")
    else:
        body = replace_tag_value(body, "identifier", data[4])

    if condition == "user_not_recognised":
        body = replace_tag_value(body, "id", "ThisIsAUser")

    if iib_body is not None and azure_body is not None:
        return headers, iib_body, azure_body
    else:
        return headers, body


def sc813_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC813", {"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC813 test data found for environment: {ENVIRONMENT}, condition: {condition}")

    client_number = str(data[2]).strip().zfill(9)
    swiftt_user = str(data[3]).strip()

    return {
        "request_body": payloads.sc813.get_payload_sc813(client_number=client_number, swiftt_user=swiftt_user),
        "header": payloads.sc813.get_headers_sc813(),
        "condition": condition
    }


def sc156_payload_setup(condition="all_proxy_records_created"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC156", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC156 test data was found for condition: {condition}")

    client_number = scenario_data[3]
    proxy_codes = scenario_data[4]
    proxy_date = scenario_data[5]
    benefit_type = scenario_data[6]
    process_type = scenario_data[7]
    security_token_id = scenario_data[8]

    correlation_id = str(uuid.uuid4())
    source_system = "CMS"

    proxy_code_list = [proxy_code.strip() for proxy_code in proxy_codes.split(",") if proxy_code.strip()]

    proxy_details = []

    for proxy_code in proxy_code_list:
        proxy_details.append(
            {
                "action_type": "CREATE",
                "reference_id": str(uuid.uuid4()),
                "proxy_code": proxy_code,
                "proxy_date": proxy_date
            }
        )

    if condition == "missing_source_system":
        source_system = None

    raise_error = condition != "invalid_client_number"

    return {
        "request_body": payloads.sc156.get_payload_sc156(
            client_number=client_number,
            correlation_id=correlation_id,
            proxy_details=proxy_details,
            benefit_type=benefit_type,
            process_type=process_type,
            security_token_id=security_token_id,
            source_system=source_system
        ),
        "header": payloads.sc156.get_headers_sc156(),
        "condition": condition,
        "client_number": client_number,
        "correlation_id": correlation_id,
        "proxy_details": proxy_details,
        "raise_error": raise_error
    }


def sc586_payload_setup(condition: str, payload_type: str):
    headers = payloads.sc586.get_headers_sc586()
    body = payloads.sc586.get_payload_sc586(payload_type=payload_type)
    body = body.replace("TRANSID", pytest.AUTO_TRANSACTION_ID)
    if payload_type in ["add_child", "edit_child"]:
        db = SqliteConnection()
        db.connect()
        try:
            data = db.get_data(
                table_name="SC586",
                column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "processing_successful_swiftt"}
            )
        finally:
            db.close()
        if data[3] != "None":
            """Generate a random number for the child swn ID"""
            child_swn = random.randint(100_000_000, 999_999_999)
            child_names = data[3].split()
            body = (
                (
                    body.replace("CHILDFIRSTNAME", child_names[0])
                    .replace("CHILDMIDDLENAME", child_names[1])
                    .replace("CHILDFAMILYNAME", child_names[2])
                )
                .replace("CHILDDOB", data[4])
                .replace("CHILDCLIENT", str(child_swn))
            )
        body = body.replace("ADULTCLIENT", data[1])
    else:
        """Generate a swn and IRD number to be used with the new client"""
        ird_num = generate_ird_number()
        client_swn = random.randint(100_000_000, 999_999_999)
        first_name = random.choice(string.ascii_letters)
        middle_name = random.choice(string.ascii_letters)
        for i in range(7):
            first_name = f"{first_name}{random.choice(string.ascii_letters)}"
            middle_name = f"{middle_name}{random.choice(string.ascii_letters)}"

        body = (
            body.replace("CLIENTIRD", ird_num)
            .replace("CLIENTSWN", str(client_swn))
            .replace("CLIENTFIRSTNAME", first_name)
            .replace("CLIENTMIDDLENAME", middle_name)
        )

    if "edit" in payload_type:
        body = replace_tag_value(body, "action", "CHG", parent_tag="publication")

    if condition == "processing_queued_wam":
        body = replace_tag_value(body, "subscriber", "WAM")
    elif condition == "19_year_old_child_swiftt" and payload_type in ["add_child", "edit_child"]:
        body = replace_tag_value(body, "dateOfBirth", "2000-08-26")
    elif condition == "effective_date_greater_than_8_week":
        body = replace_tag_value(body, "start", "2030-01-01")
    elif condition == "unexpected_error_swiftt":
        body = replace_tag_value(body, "id", "C", "securityToken")
    return headers, body


def _get_sc596_clients(required_count=4):
    results = get_from_swiftt(get_swiftt_connection_string(), swiftt_db_queries.sc596_manage_tenancy_clients_query)

    if not results:
        raise ValueError("No eligible SC596 clients were found through SWIFTT SQL")

    clients = []
    used_swns = set()

    for row in results:
        client_number = str(row[0]).strip().zfill(9)

        if client_number in used_swns:
            continue

        clients.append(
            {
                "client_number": client_number,
                "given_name": str(row[1]).strip().upper(),
                "surname": str(row[2]).strip().upper()
            }
        )

        used_swns.add(client_number)

        if len(clients) == required_count:
            break

    if len(clients) < required_count:
        raise ValueError(
            f"SC596 requires {required_count} distinct eligible clients, but only {len(clients)} were available"
        )

    return clients


def _get_sc596_sqlite_client(condition):
    db = SqliteConnection()
    db.connect()

    try:
        sc596_data = db.get_data(
            table_name="SC596", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc596_data:
        raise ValueError(f"No SC596 test data was found in SQLite for condition: {condition}")

    client_number = str(sc596_data[3]).strip().zfill(9)

    if not client_number:
        raise ValueError(f"SC596 CLIENT_NUMBER is empty for condition: {condition}")

    return client_number


def _get_sc596_sqlite_tenant_client(condition):
    db = SqliteConnection()
    db.connect()

    try:
        sc596_data = db.get_data(
            table_name="SC596", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc596_data:
        raise ValueError(f"No SC596 test data was found in SQLite for condition: {condition}")

    tenant_client_number = str(sc596_data[4]).strip().zfill(9)

    if not tenant_client_number:
        raise ValueError(f"SC596 TENANT_CLIENT_NUMBER is empty for condition: {condition}")

    return tenant_client_number


def _get_sc596_tenant_cost_mismatch_payload(condition):
    tenant_client_number = _get_sc596_sqlite_tenant_client(condition)
    head_clients = _get_sc596_clients(required_count=2)

    iib_head_client = head_clients[0]
    azure_head_client = head_clients[1]

    return {
        "iib_request_body": payloads.sc596.get_payload_sc596(
            client_number=iib_head_client["client_number"],
            tenant_client_number=tenant_client_number,
            tenant_first_name="TEST",
            tenant_surname="TEST"
        ),
        "azure_request_body": payloads.sc596.get_payload_sc596(
            client_number=azure_head_client["client_number"],
            tenant_client_number=tenant_client_number,
            tenant_first_name="TEST",
            tenant_surname="TEST"
        ),
        "header": payloads.sc596.get_headers_sc596()
    }


def _get_sc596_negative_payload(condition):
    head_client_number = _get_sc596_sqlite_client(condition)

    tenants = _get_sc596_clients(required_count=2)

    iib_tenant_client = tenants[0]
    azure_tenant_client = tenants[1]

    return {
        "iib_request_body": payloads.sc596.get_payload_sc596(
            client_number=head_client_number,
            tenant_client_number=iib_tenant_client["client_number"],
            tenant_first_name=iib_tenant_client["given_name"],
            tenant_surname=iib_tenant_client["surname"]
        ),
        "azure_request_body": payloads.sc596.get_payload_sc596(
            client_number=head_client_number,
            tenant_client_number=azure_tenant_client["client_number"],
            tenant_first_name=azure_tenant_client["given_name"],
            tenant_surname=azure_tenant_client["surname"]
        ),
        "header": payloads.sc596.get_headers_sc596()
    }


def _apply_sc596_validation(request_body, condition):
    if isinstance(request_body, str):
        body = json.loads(request_body)
    else:
        body = copy.deepcopy(request_body)

    tenancy = body["data"]["tenancy"]
    tenant = tenancy["tenants"][0]

    if condition == "weekly_accommodation_cost_missing":
        tenancy.pop("weeklyAccommodationCost", None)

    elif condition == "duplicate_tenant":
        tenancy["tenants"].append(copy.deepcopy(tenant))

    elif condition == "given_names_not_uppercase_or_alphabetic":
        tenant["firstName"] = "Test1"

    elif condition == "name_or_surname_exceeds_30_characters":
        tenant["firstName"] = "A" * 31

    elif condition == "given_names_start_with_space":
        tenant["firstName"] = " TEST"

    elif condition == "given_names_missing":
        tenant.pop("firstName", None)

    elif condition == "surname_not_uppercase_or_alphabetic":
        tenant["surname"] = "Test1"

    elif condition == "surname_missing":
        tenant.pop("surname", None)

    elif condition == "cost_type_missing":
        tenant.pop("costType", None)

    elif condition == "cost_missing":
        tenant.pop("costAmount", None)

    elif condition == "cost_frequency_missing":
        tenant.pop("costFrequency", None)

    elif condition == "start_date_missing":
        tenant.pop("startDate", None)

    elif condition == "household_total_proportion_exceeds_100":
        tenant["homeProportion"] = 101

    elif condition == "swn_and_surname_missing":
        tenant.pop("clientNumber", None)
        tenant.pop("surname", None)

    else:
        raise ValueError(f"SC596 validation condition is not implemented yet: {condition}")

    return json.dumps(body)


def _get_sc596_validation_payload(condition):
    clients = _get_sc596_clients(required_count=4)

    iib_head_client = clients[0]
    iib_tenant_client = clients[1]
    azure_head_client = clients[2]
    azure_tenant_client = clients[3]

    iib_request_body = payloads.sc596.get_payload_sc596(
        client_number=iib_head_client["client_number"],
        tenant_client_number=iib_tenant_client["client_number"],
        tenant_first_name=iib_tenant_client["given_name"],
        tenant_surname=iib_tenant_client["surname"]
    )

    azure_request_body = payloads.sc596.get_payload_sc596(
        client_number=azure_head_client["client_number"],
        tenant_client_number=azure_tenant_client["client_number"],
        tenant_first_name=azure_tenant_client["given_name"],
        tenant_surname=azure_tenant_client["surname"]
    )

    return {
        "iib_request_body": _apply_sc596_validation(iib_request_body, condition),
        "azure_request_body": _apply_sc596_validation(azure_request_body, condition),
        "header": payloads.sc596.get_headers_sc596()
    }


def sc596_payload_setup(condition="successful_response"):
    if condition == "successful_response":
        clients = _get_sc596_clients()

        iib_head_client = clients[0]
        iib_tenant_client = clients[1]
        azure_head_client = clients[2]
        azure_tenant_client = clients[3]

        return {
            "iib_request_body": payloads.sc596.get_payload_sc596(
                client_number=iib_head_client["client_number"],
                tenant_client_number=iib_tenant_client["client_number"],
                tenant_first_name=iib_tenant_client["given_name"],
                tenant_surname=iib_tenant_client["surname"]
            ),
            "azure_request_body": payloads.sc596.get_payload_sc596(
                client_number=azure_head_client["client_number"],
                tenant_client_number=azure_tenant_client["client_number"],
                tenant_first_name=azure_tenant_client["given_name"],
                tenant_surname=azure_tenant_client["surname"]
            ),
            "header": payloads.sc596.get_headers_sc596()
        }

    elif condition in (
        "client_not_recognised",
        "client_without_eligible_service",
        "client_with_linked_active_tenant_records",
        "client_is_apportioned_partner"
    ):
        return _get_sc596_negative_payload(condition)

    elif condition == "tenant_cost_does_not_match_sup_cost":
        return _get_sc596_tenant_cost_mismatch_payload(condition)

    elif condition in (
        "weekly_accommodation_cost_missing",
        "weekly_accommodation_cost_invalid",
        "business_expenses_invalid",
        "duplicate_tenant",
        "given_names_not_uppercase_or_alphabetic",
        "name_or_surname_exceeds_30_characters",
        "given_names_start_with_space",
        "given_names_missing",
        "surname_not_uppercase_or_alphabetic",
        "surname_missing",
        "cost_type_missing",
        "cost_missing",
        "cost_frequency_missing",
        "start_date_invalid",
        "start_date_missing",
        "date_overlaps_previous_record",
        "end_date_invalid",
        "proportion_invalid_for_non_renter_or_nap",
        "nap_proportion_missing",
        "household_total_proportion_exceeds_100",
        "renter_proportion_invalid",
        "nap_description_exceeds_50_characters",
        "tents_search_required_before_tentu",
        "swn_and_surname_missing",
        "invalid_entry_source",
        "client_linked_as_boarder_or_renter",
        "cost_frequency_invalid",
        "cost_type_invalid",
        "entry_not_via_tenti",
        "client_already_linked_as_tenant",
        "start_date_before_head_tenant_dob",
        "tenant_removed_reassessment_required",
        "end_date_after_current_pay_period",
        "benefit_type_cannot_complete_action",
        "tenant_is_apportioned_partner"
    ):
        return _get_sc596_validation_payload(condition)

    raise ValueError(f"Unsupported SC596 condition: {condition}")


def sc863_payload_setup(condition: str, request_type: str):
    headers = payloads.sc863.get_headers_sc863()
    body = None
    if request_type != "cancel_appointment":
        body = payloads.sc863.get_payload_sc863()

        # Generate a random date within 10 days of today
        for i in range(20):
            random_date_within_20_days = datetime.now(ZoneInfo("Pacific/Auckland")) + timedelta(
                days=random.randint(0, 20)
            )
            # make sure the day selected is a weekday
            if random_date_within_20_days.weekday() < 5:
                formatted_date = random_date_within_20_days.strftime("%Y-%m-%d")
                break
        else:
            raise RuntimeError("Failed to generate a weekday date")
        # Generate a start and end time with the end time being 30mins after the start
        opening_hours = datetime.strptime("08:30", "%H:%M")
        closing_hours = datetime.strptime("16:30", "%H:%M")
        total_slots = int((closing_hours - opening_hours).total_seconds() // (5 * 60))
        if condition == "timeslot_not_available_preferred_office":
            body = body.replace('"identifier" : ""', '"identifier" : "KSTEV024"')
            start_time = "2026-09-04T12:00"
            end_time = "2026-09-04T12:30"
            body = body.replace("<AppStartDate>T<AppStartTime>", f"{start_time}").replace(
                "<AppEndDate>T<AppEndTime>", f"{end_time}"
            )
        else:
            start_time = opening_hours + timedelta(minutes=random.randint(0, total_slots) * 5)
            end_time = start_time + timedelta(minutes=30)
            formatted_end_time = end_time.strftime("%H:%M")
            formatted_start_time = start_time.strftime("%H:%M")
            body = body.replace("<AppStartDate>T<AppStartTime>", f"{formatted_date}T{formatted_start_time}").replace(
                "<AppEndDate>T<AppEndTime>", f"{formatted_date}T{formatted_end_time}"
            )

        if condition == "timeslot_not_available_with_staff_member":
            body = body.replace('"locationRefId" : "CASL"', '"locationRefId" : "WCBH"')
            body = body.replace('"identifier" : ""', '"identifier" : "bfaap001"')
            body = body.replace("<AppStartDate>T<AppStartTime>", "2026-12-01T11:30").replace(
                "<AppEndDate>T<AppEndTime>", "2024-12-01T12:00"
            )

    if condition == "error_401_client_auth_failed":
        del headers["Authorization"]

    if body is None:
        return headers, None
    else:
        return headers, json.loads(body)


def dp863_payload_setup(condition: str, request_type: str):
    headers = payloads.sc863.get_headers_sc863()
    body = None
    if request_type != "cancel_appointment":
        body = payloads.sc863.get_payload_sc863()

        # Generate a random date within 10 days of today
        for i in range(20):
            random_date_within_20_days = datetime.now(ZoneInfo("Pacific/Auckland")) + timedelta(
                days=random.randint(0, 20)
            )
            # make sure the day selected is a weekday
            if random_date_within_20_days.weekday() < 5:
                formatted_date = random_date_within_20_days.strftime("%Y-%m-%d")
                break
        else:
            raise RuntimeError("Failed to generate a weekday date")
        # Generate a start and end time with the end time being 30mins after the start
        opening_hours = datetime.strptime("08:30", "%H:%M")
        closing_hours = datetime.strptime("17:00", "%H:%M")
        total_slots = int((closing_hours - opening_hours).total_seconds() // (5 * 60))
        if condition == "timeslot_not_available_preferred_office":
            body = body.replace('"identifier" : ""', '"identifier" : "KSTEV024"')
            start_time = "2026-09-04T12:00"
            end_time = "2026-09-04T12:30"
            body = body.replace("<AppStartDate>T<AppStartTime>", f"{start_time}").replace(
                "<AppEndDate>T<AppEndTime>", f"{end_time}"
            )
        else:
            start_time = opening_hours + timedelta(minutes=random.randint(0, total_slots) * 5)
            end_time = start_time + timedelta(minutes=30)
            formatted_end_time = end_time.strftime("%H:%M")
            formatted_start_time = start_time.strftime("%H:%M")
            body = body.replace("<AppStartDate>T<AppStartTime>", f"{formatted_date}T{formatted_start_time}").replace(
                "<AppEndDate>T<AppEndTime>", f"{formatted_date}T{formatted_end_time}"
            )

        if condition == "timeslot_not_available_with_staff_member":
            body = body.replace('"locationRefId" : "CASL"', '"locationRefId" : "WCBH"')
            body = body.replace('"identifier" : ""', '"identifier" : "bfaap001"')
            body = body.replace("<AppStartDate>T<AppStartTime>", "2026-12-01T11:30").replace(
                "<AppEndDate>T<AppEndTime>", "2024-12-01T12:00"
            )

    if condition == "error_401_client_auth_failed":
        del headers["Authorization"]

    if body is None:
        return headers, None
    else:
        return headers, json.loads(body)


def sc862_payload_setup(condition: str = None):
    headers = payloads.sc862.get_sc862_headers()
    params = payloads.sc862.get_sc862_params()
    if condition == "error_400_bad_request":
        params["searchFrom"] = f"{params['searchFrom']}1"

    return headers, params


def dp862_payload_setup(condition: str = None):
    headers = payloads.dp862.get_dp862_headers()
    params = payloads.dp862.get_dp862_params()
    if condition == "error_400_bad_request":
        params["searchFrom"] = f"{params['searchFrom']}1"

    return headers, params


def sc861_payload_setup(condition: str = None):
    headers = payloads.sc861.get_headers_sc861()
    body = payloads.sc861.get_payload_sc861()
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC861", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()

    body = replace_tag_value(body, "clientNumber", data[1])
    return headers, body


def dp861_payload_setup(condition: str = None):
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC861", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()
    headers = payloads.dp861.dp861_headers()
    params = payloads.dp861.dp861_params(data[1])
    return headers, params


def sc818_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc818_data = db.get_data(
            table_name="SC818", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc818_data:
        raise ValueError(f"No SC818 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc818.get_payload_sc818(user_id=sc818_data[3], privilege_type_code=sc818_data[4]),
        "header": payloads.sc818.get_headers_sc818(),
        "raise_error": True
    }


def sc897_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC897", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC897 test data was found in SQLite for condition: {condition}")

    client_number = scenario_data[3]

    return {
        "request_body": payloads.sc897.get_payload_sc897(client_number=client_number),
        "header": payloads.sc897.get_headers_sc897(),
        "raise_error": True
    }


def sc816_payload_setup(condition="client_authorisation_inactive"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC816", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC816 test data was found in SQLite for condition: {condition}")

    user_type = scenario_data[3]
    business_key = str(scenario_data[4])
    status_code = scenario_data[5]
    reason_code = scenario_data[6]
    source_system = scenario_data[7]

    return {
        "request_body": payloads.sc816.get_payload_sc816(
            business_key=business_key,
            user_type=user_type,
            status_code=status_code,
            reason_code=reason_code,
            source_system=source_system
        ),
        "header": payloads.sc816.get_headers_sc816(),
        "raise_error": True
    }


def sc817_payload_setup(condition="successful_client_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC817", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC817 test data was found in SQLite for condition: {condition}")

    user_type = scenario_data[3]
    user_id = str(scenario_data[4])
    business_key = str(scenario_data[5])
    otp = str(scenario_data[6])
    source_system = scenario_data[7]
    ip_address = scenario_data[8]
    session_identifier = scenario_data[9]

    return {
        "request_body": payloads.sc817.get_payload_sc817(
            user_type=user_type,
            user_id=user_id,
            business_key=business_key,
            otp=otp,
            source_system=source_system,
            ip_address=ip_address,
            session_identifier=session_identifier
        ),
        "header": payloads.sc817.get_headers_sc817(),
        "raise_error": True
    }


def sc896_payload_setup(condition: str = None):
    headers = payloads.sc896.get_headers_sc896()
    body = payloads.sc896.get_payload_sc896()
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC896", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()

    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    if condition == "missing_swn":
        body = replace_tag_value(body, "id", "")
    else:
        body = replace_tag_value(body, "id", data[1])

    return headers, body


def dp896_payload_setup(condition: str = None):
    headers = payloads.dp896.get_headers_dp896()
    params = payloads.dp896.get_params_dp896()
    body = payloads.dp896.get_payload_dp896()

    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC896", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()

    if condition == "missing_swn":
        body = body.replace("SWN", "")
    else:
        body = body.replace("SWN", data[1])

    return headers, params, body


def sc730_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC730", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC730 test data was found in SQLite for condition: {condition}")

    client_number = scenario_data[3] or ""
    csv_scanned_image_ref = scenario_data[4] or ""
    created_by = scenario_data[5] or None

    if condition == "duplicate_document_reference":
        scanned_image_ref_iib = csv_scanned_image_ref
        scanned_image_ref_azure = csv_scanned_image_ref

    elif condition == "missing_mandatory_data":
        scanned_image_ref_iib = ""
        scanned_image_ref_azure = ""

    else:
        scanned_image_ref_iib = payloads.sc730.generate_sc730_scanned_image_ref()
        scanned_image_ref_azure = payloads.sc730.generate_sc730_scanned_image_ref()

    request_body_iib = payloads.sc730.get_payload_sc730(
        client_number=client_number, scanned_image_ref=scanned_image_ref_iib, created_by=created_by
    )

    request_body_azure = payloads.sc730.get_payload_sc730(
        client_number=client_number, scanned_image_ref=scanned_image_ref_azure, created_by=created_by
    )

    return {
        "request_body_iib": request_body_iib,
        "request_body_azure": request_body_azure,
        "header": payloads.sc730.get_headers_sc730(),
        "raise_error": True
    }


def sc891_payload_setup(condition="no_further_action"):
    db = SqliteConnection()
    db.connect()

    try:
        sc891_data = db.get_data(
            table_name="SC891", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc891_data:
        raise ValueError(f"No SC891 test data was found in SQLite for condition: {condition}")

    audit_id = str(uuid4())
    correlation_id = str(uuid4())

    return {
        "request_body": payloads.sc891.get_payload_sc891(
            audit_id=audit_id,
            correlation_id=correlation_id,
            client_number=sc891_data[3],
            callback_address=sc891_data[4]
        ),
        "header": payloads.sc891.get_headers_sc891(),
        "raise_error": True
    }


def sc890_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc890.get_payload_sc890(),
        "header": payloads.sc890.get_headers_sc890(),
        "condition": condition
    }


def sc834_payload_setup(condition: str, current_notification_id: str = None):
    headers = payloads.sc834.get_headers_sc834()
    body = payloads.sc834.get_payload_sc834()
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(
            table_name="SC834", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
        )
        if current_notification_id is not None and condition != "no_notification_found":
            if current_notification_id == data[2]:
                for i in range(10):
                    data = db.get_data(
                        table_name="SC834",
                        column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
                    )
                    if current_notification_id != data[2]:
                        break
                    elif current_notification_id == data[2] and i == 9:
                        raise Exception(
                            "Could not find another notification id for the azure payload, run SC831 to create more"
                        )
    finally:
        db.close()

    body = replace_tag_value(body, "id", data[1], "participant")
    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    if condition == "no_notification_found":
        body = replace_tag_value(body, "notificationId", "8623b214-8653-490d-bddf-b40fffc9d7b4")
    elif condition == "notification_not_recognised":
        body = replace_tag_value(body, "notificationId", "not_a_notification_id")
    else:
        body = replace_tag_value(body, "notificationId", data[2])

    return headers, body, data[2]


def dp834_payload_setup(condition: str, current_notification_id: str = None):
    headers = payloads.dp834.get_headers_dp834()
    body = payloads.dp834.get_payload_dp834()
    params = payloads.dp834.get_params_dp834()

    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(
            table_name="SC834", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
        )
        if current_notification_id is not None and condition != "no_notification_found":
            if current_notification_id == data[2]:
                for i in range(10):
                    data = db.get_data(
                        table_name="SC834",
                        column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
                    )
                    if current_notification_id != data[2]:
                        break
                    elif current_notification_id == data[2] and i == 9:
                        raise Exception(
                            "Could not find another notification id for the azure payload, run SC831 to create more"
                        )
    finally:
        db.close()

    body = body.replace("SWN", data[1])

    if condition == "no_notification_found":
        body = body.replace("NOTIFICATION_ID", "8623b214-8653-490d-bddf-b40fffc9d7b4")
    elif condition == "notification_not_recognised":
        body = body.replace("NOTIFICATION_ID", "not_a_notification_id")
    else:
        body = body.replace("NOTIFICATION_ID", data[2])

    return headers, body, params, data[2]


def sc835_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc835.get_payload_sc835(),
        "header": payloads.sc835.get_headers_sc835(),
        "condition": condition
    }


def sc831_payload_setup(condition: str, payload_type: str):
    headers = payloads.sc831.get_headers_sc831()
    body = payloads.sc831.get_payload_sc831(payload_type=payload_type)

    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(
            table_name="SC831", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
        )
    finally:
        db.close()
    body = body.replace("SWN", data[1]).replace("TRANSID", pytest.AUTO_TRANSACTION_ID)

    if condition == "maximum_character_limit_email_body" and payload_type == "email_and_attachment_notification":
        characters = string.ascii_letters + string.digits
        long_string = "".join(random.choices(characters, k=8001))
        body = body.replace("EMAILBODYTEXT", long_string)
    elif condition == "invalid_text_format":
        body = body.replace("HTML", "BOB")
    elif condition == "document_name_not_specified" and payload_type == "email_and_attachment_notification":
        body = body.replace("docName", "")
    elif condition == "file_extension_not_specified":
        body = body.replace("<v15:fileExtension>pdf</v15:fileExtension>", "<v15:fileExtension></v15:fileExtension>")

    return headers, body, data[1]


def dp831_payload_setup(condition: str):
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(
            table_name="SC831", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": "transaction_successful"}
        )
    finally:
        db.close()

    headers = payloads.dp831.get_headers_dp831()
    body = payloads.dp831.get_payload_dp831(data[1])
    params = payloads.dp831.get_params_dp831()

    return headers, body, params


def sc832_payload_setup(condition="successful_response"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC832", {"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC832 test data found for environment '{ENVIRONMENT}' and condition '{condition}'")

    # SC832.csv
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = SOURCE_SYSTEM
    # 3 = ACTIVITY_CODE
    # 4 = PHONE_NUMBER

    source_system = data[2]
    activity_code = data[3]
    phone_number = str(data[4])

    return {
        "request_body": payloads.sc832.get_payload_sc832(
            source_system=source_system,
            activity_code=activity_code,
            phone_number=phone_number,
            transaction_id=pytest.AUTO_TRANSACTION_ID
        ),
        "header": payloads.sc832.get_headers_sc832(),
        "condition": condition
    }


def sc833_payload_setup(condition: str = None):
    headers = payloads.sc833.get_headers_sc833()
    body = payloads.sc833.get_payload_sc833()
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC833", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()

    body = replace_tag_value(body, "transactionId", pytest.AUTO_TRANSACTION_ID)
    body = replace_tag_value(body, "id", data[1], "participant")

    return headers, body


def dp833_payload_setup(condition: str = None):
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC833", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()
    headers = payloads.dp833.get_headers_dp833()
    params = payloads.dp833.get_params_dp833(data[1])

    return headers, params


def sc720_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc720.get_payload_sc720(),
        "header": payloads.sc720.get_headers_sc720(),
        "condition": condition
    }


def sc345_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc345.get_payload_sc345(),
        "header": payloads.sc345.get_headers_sc345(),
        "condition": condition
    }


def sc845_payload_setup(condition: str = None):
    headers = payloads.sc845.get_headers_sc845()
    body = payloads.sc845.get_sc845_body()
    db = SqliteConnection()
    db.connect()
    try:
        data = db.get_data(table_name="SC845", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition})
    finally:
        db.close()
    body = replace_tag_value(body, "clientNumber", data[1])

    return headers, body


def sc801_payload_setup(condition="successful_transaction"):
    db = SqliteConnection()
    db.connect()

    try:
        data = db.get_data(table_name="SC801", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition})
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC801 test data found for condition: {condition}")

    client_number = data[2]
    start_date = data[3]
    end_date = data[4]

    return {
        "request_body": payloads.sc801.get_payload_sc801(
            condition=condition, client_number=client_number, start_date=start_date, end_date=end_date
        ),
        "header": payloads.sc801.get_headers_sc801(),
        "condition": condition
    }


def sc865_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc865.get_payload_sc865(),
        "header": payloads.sc865.get_headers_sc865(),
        "condition": condition
    }


def sc803_payload_setup(condition="successful_transaction"):

    if condition == "successful_transaction":
        results = get_from_swiftt(get_swiftt_connection_string(), swiftt_db_queries.SC803_SUCCESSFUL_TRANSACTION_CLIENT)

        if not results or len(results) < 2:
            raise ValueError("Eligible SC803 clients are required for successful_transaction")

        iib_client_number = str(results[0][0]).zfill(9)
        azure_client_number = str(results[1][0]).zfill(9)

        iib_request_body = payloads.sc803.get_payload_sc803(client_number=iib_client_number)

        azure_request_body = payloads.sc803.get_payload_sc803(client_number=azure_client_number)

    else:
        db_conn = SqliteConnection()
        db_conn.connect()

        try:
            data = db_conn.get_data("SC803", {"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition})
        finally:
            db_conn.close()

        if not data:
            raise ValueError(f"No SC803 test data found for condition: {condition}")

        client_number = str(data[2]).zfill(9)

        iib_client_number = client_number
        azure_client_number = client_number

        request_body = payloads.sc803.get_payload_sc803(client_number=client_number)

        iib_request_body = request_body
        azure_request_body = request_body

    headers = payloads.sc803.get_headers_sc803()
    headers["MSD-Sub-Env"] = "d11"

    return {
        "iib_request_body": iib_request_body,
        "azure_request_body": azure_request_body,
        "header": headers,
        "iib_client_number": iib_client_number,
        "azure_client_number": azure_client_number,
        "condition": condition
    }


def sc846_payload_setup(condition="successful_transaction"):
    nz_timezone = ZoneInfo("Pacific/Auckland")

    request_date_time = datetime.now(nz_timezone).isoformat(timespec="seconds")

    effective_date = datetime.now(nz_timezone).strftime("%Y-%m-%d")

    if condition == "successful_transaction":
        results = get_from_swiftt(get_swiftt_connection_string(), swiftt_db_queries.SC846_SUCCESSFUL_TRANSACTION_CLIENT)

        if not results or len(results) < 2:
            raise ValueError("Less than 2 suitable SC846 clients found for successful_transaction")

        # Two different clients because APPLYSANCTION changes client state
        client_number_iib = str(results[0][0]).zfill(9)
        client_number_azure = str(results[1][0]).zfill(9)

        change_reason = "OF1"
        change_type = "APPLYSANCTION"

    else:
        db_conn = SqliteConnection()
        db_conn.connect()

        try:
            data = db_conn.get_data(
                table_name="SC846", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
            )
        finally:
            db_conn.close()

        if not data:
            raise ValueError(f"No SC846 test data found for condition: {condition}")

        client_number_iib = str(data[2]).zfill(9)
        client_number_azure = client_number_iib

        change_reason = data[3]
        change_type = data[4]

    audit_id = str(uuid4())
    correlation_id = str(uuid4())

    if condition == "obligation_failure_id_not_supplied":
        reference = None
    else:
        reference = str(uuid4())

    request_body_iib = payloads.sc846.get_payload_sc846(
        audit_id=audit_id,
        correlation_id=correlation_id,
        request_date_time=request_date_time,
        client_number=client_number_iib,
        effective_date=effective_date,
        change_reason=change_reason,
        change_type=change_type,
        reference=reference
    )

    request_body_azure = payloads.sc846.get_payload_sc846(
        audit_id=audit_id,
        correlation_id=correlation_id,
        request_date_time=request_date_time,
        client_number=client_number_azure,
        effective_date=effective_date,
        change_reason=change_reason,
        change_type=change_type,
        reference=reference
    )

    return {
        "request_body_iib": request_body_iib,
        "request_body_azure": request_body_azure,
        "header": payloads.sc846.get_headers_sc846(),
        "condition": condition,
        "client_number_iib": client_number_iib,
        "client_number_azure": client_number_azure,
        "change_reason": change_reason,
        "change_type": change_type,
        "reference": reference
    }


def sc866_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc866.get_payload_sc866(),
        "header": payloads.sc866.get_headers_sc866(),
        "condition": condition
    }


def sc836_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc836_data = db.get_data(
            table_name="SC836", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc836_data:
        raise ValueError(f"No SC836 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc836.get_payload_sc836(
            client_number=sc836_data[3], originating_system_reference_id=sc836_data[4], created_by=sc836_data[5]
        ),
        "header": payloads.sc836.get_headers_sc836(),
        "raise_error": True
    }


def sc815_payload_setup(condition="successful_client_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC815", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC815 test data was found in SQLite for condition: {condition}")

    user_type = scenario_data[3]
    business_key = str(scenario_data[4])
    mobile_number = str(scenario_data[5])

    return {
        "request_body": payloads.sc815.get_payload_sc815(
            business_key=business_key, mobile_number=mobile_number, user_type=user_type
        ),
        "header": payloads.sc815.get_headers_sc815(),
        "raise_error": True
    }


def sc730v2_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC730V2", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC730V2 test data was found in SQLite for condition: {condition}")

    client_number = scenario_data[3] or ""
    csv_scanned_image_ref = scenario_data[4] or ""
    security_token_id = scenario_data[5] or None

    document_sub_type = "Seniors Annual Review Evidence"

    if condition == "successful_response":
        scanned_image_ref_iib = payloads.sc730v2.generate_sc730v2_scanned_image_ref()
        scanned_image_ref_azure = payloads.sc730v2.generate_sc730v2_scanned_image_ref()

        business_transaction_id_iib = payloads.sc730v2.generate_sc730v2_business_transaction_id()
        business_transaction_id_azure = payloads.sc730v2.generate_sc730v2_business_transaction_id()

        communication_id_iib = payloads.sc730v2.generate_sc730v2_communication_id()
        communication_id_azure = payloads.sc730v2.generate_sc730v2_communication_id()

    elif condition == "duplicate_document_reference":
        scanned_image_ref_iib = csv_scanned_image_ref
        scanned_image_ref_azure = csv_scanned_image_ref

        business_transaction_id_iib = business_transaction_id_azure = (
            payloads.sc730v2.generate_sc730v2_business_transaction_id()
        )
        communication_id_iib = communication_id_azure = payloads.sc730v2.generate_sc730v2_communication_id()

    elif condition == "missing_mandatory_data":
        scanned_image_ref_iib = ""
        scanned_image_ref_azure = ""

        business_transaction_id_iib = business_transaction_id_azure = (
            payloads.sc730v2.generate_sc730v2_business_transaction_id()
        )
        communication_id_iib = communication_id_azure = payloads.sc730v2.generate_sc730v2_communication_id()

    else:
        shared_scanned_image_ref = payloads.sc730v2.generate_sc730v2_scanned_image_ref()
        scanned_image_ref_iib = scanned_image_ref_azure = shared_scanned_image_ref

        business_transaction_id_iib = business_transaction_id_azure = (
            payloads.sc730v2.generate_sc730v2_business_transaction_id()
        )
        communication_id_iib = communication_id_azure = payloads.sc730v2.generate_sc730v2_communication_id()

    if condition == "invalid_request_data":
        document_sub_type = "Annual Review"

    request_body_iib = payloads.sc730v2.get_payload_sc730v2(
        client_number=client_number,
        scanned_image_ref=scanned_image_ref_iib,
        business_transaction_id=business_transaction_id_iib,
        communication_id=communication_id_iib,
        security_token_id=security_token_id,
        document_sub_type=document_sub_type
    )

    request_body_azure = payloads.sc730v2.get_payload_sc730v2(
        client_number=client_number,
        scanned_image_ref=scanned_image_ref_azure,
        business_transaction_id=business_transaction_id_azure,
        communication_id=communication_id_azure,
        security_token_id=security_token_id,
        document_sub_type=document_sub_type
    )

    return {
        "request_body_iib": request_body_iib,
        "request_body_azure": request_body_azure,
        "header": payloads.sc730v2.get_headers_sc730v2(),
        "raise_error": True
    }


def sc731_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC731", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC731 test data was found in SQLite for condition: {condition}")

    scanned_image_ref = scenario_data[3]

    return {
        "request_body": payloads.sc731.get_payload_sc731(scanned_image_ref=scanned_image_ref),
        "header": payloads.sc731.get_headers_sc731(),
        "raise_error": True
    }


def sc732_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC732P", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC732P test data was found in SQLite for condition: {condition}")

    scanned_image_ref = scenario_data[3]

    raise_error = condition not in ["document_identifier_not_recognised", "missing_mandatory_data"]

    return {
        "request_body": payloads.sc732P.get_payload_sc732(scanned_image_ref=scanned_image_ref),
        "header": payloads.sc732P.get_headers_sc732(),
        "raise_error": raise_error
    }


def sc587_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc587_data = db.get_data(
            table_name="SC587", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc587_data:
        raise ValueError(f"No SC587 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc587.get_payload_sc587(swiftt_user_id=sc587_data[3]),
        "header": payloads.sc587.get_headers_sc587(),
        "raise_error": True
    }


def sc733p_payload_setup(condition="publish_draft_document"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC733P", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC733P test data was found in SQLite for condition: {condition}")

    scanned_image_ref = scenario_data[3]
    client_number = scenario_data[4]

    request_body = payloads.sc733p.get_payload_sc733p(scanned_image_ref=scanned_image_ref, client_number=client_number)

    if condition == "missing_mandatory_data":
        request_body = request_body.replace(f"<scannedImageRef>{scanned_image_ref}</scannedImageRef>", "")

    raise_error = condition not in ["missing_mandatory_data", "document_identifier_not_recognised"]

    return {"request_body": request_body, "header": payloads.sc733p.get_headers_sc733p(), "raise_error": raise_error}


def sc889_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        sc889_data = db.get_data(
            table_name="SC889", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not sc889_data:
        raise ValueError(f"No SC889 test data was found in SQLite for condition: {condition}")

    audit_id = str(uuid4())
    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="milliseconds")

    return {
        "request_body": payloads.sc889.get_payload_sc889(
            audit_id=audit_id,
            request_date_time=request_date_time,
            client_number=sc889_data[3],
            application_date=sc889_data[4],
            event_date=sc889_data[5],
            evidence_received_date=sc889_data[6],
            bank=sc889_data[7],
            branch=sc889_data[8],
            account=sc889_data[9],
            suffix=sc889_data[10],
            income_amount=sc889_data[11],
            product_id=sc889_data[12],
            income_type=sc889_data[13],
            entitlement_code=sc889_data[14]
        ),
        "header": payloads.sc889.get_headers_sc889(),
        "raise_error": True
    }




def sc702_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc702.get_payload_sc702(),
        "header": payloads.sc702.get_headers_sc702(),
        "condition": condition
    }


def sc331_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc331.get_payload_sc331(),
        "header": payloads.sc331.get_headers_sc331(),
        "condition": condition
    }


def sc354_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc354.get_payload_sc354(),
        "header": payloads.sc354.get_headers_sc354(),
        "condition": condition
    }


def sc341_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc341.get_payload_sc341(),
        "header": payloads.sc341.get_headers_sc341(),
        "condition": condition
    }


def sc356_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC356", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC356 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc356.get_payload_sc356(
            provider_id=scenario_data[3],
            tenancy_reference=scenario_data[4],
            new_rent=scenario_data[5],
            rent_charge_date=scenario_data[6],
            actual_rent_change_date=scenario_data[7],
            expected_rent_change_date=scenario_data[8],
            rent_change_reason=scenario_data[9],
            rent_end_date=scenario_data[10]
        ),
        "header": payloads.sc356.get_headers_sc356(),
        "raise_error": True
    }


def sc343_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc343.get_payload_sc343(),
        "header": payloads.sc343.get_headers_sc343(),
        "condition": condition
    }


def sc357_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC357", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC357 test data was found in SQLite for condition: {condition}")

    return {
        "request_body": payloads.sc357.get_payload_sc357(
            provider_id=scenario_data[3],
            tenancy_reference=scenario_data[4],
            person_identifier=scenario_data[5],
            first_name=scenario_data[6],
            family_name=scenario_data[7],
            member_type=scenario_data[8],
            effective_date=scenario_data[9],
            action=scenario_data[10]
        ),
        "header": payloads.sc357.get_headers_sc357(),
        "raise_error": True
    }


def sc358_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc358.get_payload_sc358(),
        "header": payloads.sc358.get_headers_sc358(),
        "condition": condition
    }


def sc351_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc351.get_payload_sc351(),
        "header": payloads.sc351.get_headers_sc351(),
        "condition": condition
    }


def sc348_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc348.get_payload_sc348(),
        "header": payloads.sc348.get_headers_sc348(),
        "condition": condition
    }


def sc347_payload_setup(condition="successful_response"):
    return {
        "request_body": payloads.sc347.get_payload_sc347(),
        "header": payloads.sc347.get_headers_sc347(),
        "condition": condition
    }


def sc851_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC851", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC851 test data found for condition: {condition}")

    client_number = str(scenario_data[3]).zfill(9)

    request_body = payloads.sc851.get_payload_sc851(
        client_number=client_number,
        appointment_start_date=scenario_data[4],
        appointment_end_date=scenario_data[5],
        assistance_start_date=scenario_data[6],
        assistance_end_date=scenario_data[7],
        include_obligation_failures=str(scenario_data[8]).lower() == "true",
        include_user_activity=str(scenario_data[9]).lower() == "true"
    )

    raise_error = True

    if condition == "missing_client_number":
        request_body = request_body.replace(f"<v12:clientNumber>{client_number}</v12:clientNumber>", "")
        raise_error = False

    return {"request_body": request_body, "header": payloads.sc851.get_headers_sc851(), "raise_error": raise_error}


def sc128_payload_setup(condition="successful_transaction"):
    db = SqliteConnection()
    db.connect()

    try:
        data = db.get_data(table_name="SC128", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition})
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC128 test data found for condition: {condition}")

    client_number = str(data[2]).zfill(9)

    return {
        "request_body": payloads.sc128.get_payload_sc128(client_number=client_number),
        "header": payloads.sc128.get_headers_sc128(),
        "client_number": client_number,
        "condition": condition
    }


def sc802_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(
            table_name="SC802", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db_conn.close()

    if data is None:
        raise Exception(f"SC802 payload setup failed, no suitable data found for condition: {condition}")

    # Expected SQLite column order:
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = CLIENT_NUMBER
    # 3 = BANK
    # 4 = BRANCH
    # 5 = ACCOUNT
    # 6 = SUFFIX

    client_number = str(data[2]).zfill(9)
    bank = str(data[3]).zfill(2)
    branch = str(data[4]).zfill(4)
    account = str(data[5]).zfill(7)
    suffix = str(data[6]).zfill(3)

    return {
        "request_body": payloads.sc802.get_payload_sc802(
            client_number=client_number, bank=bank, branch=branch, account=account, suffix=suffix
        ),
        "header": payloads.sc802.get_headers_sc802()
    }


def sc874_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(
            table_name="SC874", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db_conn.close()

    if data is None:
        raise Exception(
            f"SC874 payload setup failed, no suitable data found for environment: {ENVIRONMENT}, condition: {condition}"
        )

    # Expected SQLite column order:
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = CLIENT_NUMBER
    # 3 = MEDICAL_CERTIFICATE_IDENTIFIER

    client_number = str(data[2]).zfill(9)
    medical_certificate_identifier = str(data[3])

    user_id = "bpmsystemuser"

    if condition == "user_not_recognised":
        user_id = "test"

    audit_id = str(uuid4())
    correlation_id = str(uuid4())

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    body = payloads.sc874.get_payload_sc874(
        client_number=client_number,
        medical_certificate_identifier=medical_certificate_identifier,
        user_id=user_id,
        audit_id=audit_id,
        correlation_id=correlation_id,
        request_date_time=request_date_time
    )

    header = payloads.sc874.get_headers_sc874()

    return {"request_body": body, "header": header}


def sc877_payload_setup(condition="successful_transaction"):
    supported_conditions = {
        "successful_transaction",
        "unsuccessful_transaction",
        "client_not_recognised",
        "cnp_id_not_recognised"
    }

    if condition not in supported_conditions:
        raise ValueError(f"Unsupported SC877 condition: {condition}")

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data_condition = condition

        # CNP ID scenario can use the successful client data.Only the user ID/retrieveSwifttUser values need to change.
        if condition == "cnp_id_not_recognised":
            data_condition = "successful_transaction"

        data = db_conn.get_data(
            table_name="SC877", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": data_condition}
        )
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC877 test data found for environment {ENVIRONMENT} and condition {data_condition}")

    # SC877 table:
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = CLIENT_NUMBER
    client_number = str(data[2]).zfill(9)

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%dT%H:%M:%S%z")

    request_date_time = request_date_time[:-2] + ":" + request_date_time[-2:]

    include_second_income = condition == "successful_transaction"

    # Default values for SC877 scenarios
    user_id = "GEKAS"
    retrieve_swiftt_user = False

    if condition == "cnp_id_not_recognised":
        user_id = "INVALID"
        retrieve_swiftt_user = True

    return {
        "request_body": payloads.sc877.get_payload_sc877(
            client_number=client_number,
            request_date_time=request_date_time,
            include_second_income=include_second_income,
            user_id=user_id,
            retrieve_swiftt_user=retrieve_swiftt_user
        ),
        "header": payloads.sc877.get_headers_sc877(),
        "client_number": client_number,
        "condition": condition
    }


def sc868_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC868", {"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC868 test data found for environment '{ENVIRONMENT}' and condition '{condition}'")

    # SQLite column order:
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = CLIENT_NUMBER
    # 3 = PAYMENT_CARD_NUMBER
    # 4 = FAMILY_NAME
    # 5 = FIRST_NAME

    client_number = str(data[2]).zfill(9)
    payment_card_number = str(data[3])
    family_name = str(data[4])
    first_name = str(data[5])

    audit_id = str(uuid4())
    correlation_id = str(uuid4())
    transaction_id = pytest.AUTO_TRANSACTION_ID

    request_date_time = datetime.now(ZoneInfo("Pacific/Auckland")).isoformat(timespec="seconds")

    application_date = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%d")

    if condition == "invalid_request":
        audit_id = ""
        transaction_id = ""

    elif condition != "successful_transaction":
        raise ValueError(f"Unsupported SC868 condition: {condition}")

    body = payloads.sc868.get_payload_sc868(
        client_number=client_number,
        payment_card_number=payment_card_number,
        family_name=family_name,
        first_name=first_name,
        audit_id=audit_id,
        correlation_id=correlation_id,
        transaction_id=transaction_id,
        request_date_time=request_date_time,
        application_date=application_date
    )

    return {
        "request_body": body,
        "header": payloads.sc868.get_headers_sc868(),
        "condition": condition,
        "client_number": client_number
    }


def sc813_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC813", {"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC813 test data found for environment: {ENVIRONMENT}, condition: {condition}")

    # SC813 table:
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = CLIENT_NUMBER
    # 3 = SWIFTT_USER

    client_number = str(data[2]).zfill(9)
    swiftt_user = str(data[3])

    return {
        "request_body": payloads.sc813.get_payload_sc813(client_number=client_number, swiftt_user=swiftt_user),
        "header": payloads.sc813.get_headers_sc813()
    }


def dp868_payload_setup(condition="successful_transaction"):
    if condition != "successful_transaction":
        raise ValueError(f"Unsupported DP868 condition: {condition}")

    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC868", {"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC868 test data found for environment '{ENVIRONMENT}' and condition '{condition}'")

    # SC868.csv
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = CLIENT_NUMBER
    # 3 = PAYMENT_CARD_NUMBER
    # 4 = FAMILY_NAME
    # 5 = FIRST_NAME

    client_number = str(data[2]).zfill(9)
    payment_card_number = str(data[3])
    family_name = str(data[4])
    first_name = str(data[5])

    application_date = datetime.now(ZoneInfo("Pacific/Auckland")).strftime("%Y-%m-%d")

    header = payloads.dp868.get_headers_dp868()
    header["MSD-Sub-Env"] = os.getenv("API_TEST_ENV", "d11")

    return {
        "request_body": payloads.dp868.get_payload_dp868(
            client_number=client_number,
            payment_card_number=payment_card_number,
            family_name=family_name,
            first_name=first_name,
            application_date=application_date
        ),
        "header": header,
        "params": payloads.dp868.get_params_dp868(transaction_id=pytest.AUTO_TRANSACTION_ID),
        "client_number": client_number,
        "transaction_id": pytest.AUTO_TRANSACTION_ID,
        "condition": condition
    }


def sc810v2_payload_setup(condition="successful_transaction"):
    nz_timezone = ZoneInfo("Pacific/Auckland")

    request_date_time = datetime.now(nz_timezone).isoformat(timespec="seconds")

    if condition == "successful_transaction":
        query = swiftt_db_queries.SC810_SUCCESSFUL_TRANSACTION_CLIENT

        results = get_from_swiftt(get_swiftt_connection_string(), query)

        if not results or len(results) < 2:
            raise ValueError("SC810V2 successful_transaction requires two suitable clients")

        iib_client_number = str(results[0][0]).zfill(9)
        iib_effective_date = results[0][1]

        azure_client_number = str(results[1][0]).zfill(9)
        azure_effective_date = results[1][1]

        if iib_effective_date.tzinfo is None:
            iib_effective_date = iib_effective_date.replace(tzinfo=nz_timezone)

        if azure_effective_date.tzinfo is None:
            azure_effective_date = azure_effective_date.replace(tzinfo=nz_timezone)

        iib_effective_date_time = iib_effective_date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(
            timespec="seconds"
        )

        azure_effective_date_time = azure_effective_date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(
            timespec="seconds"
        )

        return {
            "iib_request_body": payloads.sc810v2.get_payload_sc810v2(
                client_number=iib_client_number,
                request_date_time=request_date_time,
                effective_date_time=iib_effective_date_time
            ),
            "azure_request_body": payloads.sc810v2.get_payload_sc810v2(
                client_number=azure_client_number,
                request_date_time=request_date_time,
                effective_date_time=azure_effective_date_time
            ),
            "header": payloads.sc810v2.get_headers_sc810v2(),
            "condition": condition,
            "iib_client_number": iib_client_number,
            "azure_client_number": azure_client_number,
            "iib_effective_date_time": iib_effective_date_time,
            "azure_effective_date_time": azure_effective_date_time
        }

    elif condition == "client_not_recognised":
        db_conn = SqliteConnection()
        db_conn.connect()

        try:
            data = db_conn.get_data(
                table_name="SC810_V2", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
            )
        finally:
            db_conn.close()

        if not data:
            raise ValueError("No SC810V2 test data found for client_not_recognised")

        client_number = str(data[2]).zfill(9)
        effective_date = datetime.now(nz_timezone)

    elif condition == "income_record_already_held":
        query = swiftt_db_queries.SC810_INCOME_ALREADY_HELD_CLIENT

        results = get_from_swiftt(get_swiftt_connection_string(), query)

        if not results:
            raise ValueError("No suitable SC810V2 client found for income_record_already_held")

        client_number = results[0][0]
        effective_date = results[0][1]

    elif condition == "client_not_receiving_main_benefit":
        db_conn = SqliteConnection()
        db_conn.connect()

        try:
            data = db_conn.get_data(
                table_name="SC810_V2", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
            )
        finally:
            db_conn.close()

        if not data:
            raise ValueError("No SC810V2 test data found for client_not_receiving_main_benefit")

        client_number = str(data[2]).zfill(9)
        effective_date = datetime.now(nz_timezone)

    else:
        raise ValueError(f"Unsupported SC810V2 condition: {condition}")

    client_number = str(client_number).zfill(9)

    if effective_date.tzinfo is None:
        effective_date = effective_date.replace(tzinfo=nz_timezone)

    effective_date_time = effective_date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(
        timespec="seconds"
    )

    request_body = payloads.sc810v2.get_payload_sc810v2(
        client_number=client_number, request_date_time=request_date_time, effective_date_time=effective_date_time
    )

    return {
        "iib_request_body": request_body,
        "azure_request_body": request_body,
        "header": payloads.sc810v2.get_headers_sc810v2(),
        "condition": condition,
        "client_number": client_number,
        "effective_date_time": effective_date_time
    }


def sc702_payload_setup(condition="successful_response"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC702", {"ENVIRONMENT": "dev11", "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC702 test data found for condition: {condition}")

    # SC702.csv
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = BARCODE

    barcode = str(data[2])

    return {
        "request_body": payloads.sc702.get_payload_sc702(barcode=barcode),
        "header": payloads.sc702.get_headers_sc702()
    }


def sc852_payload_setup(condition="successful_response"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(
            "SC852",
            {
                "ENVIRONMENT": ENVIRONMENT,
                "CONDITION": condition,
            },
        )
    finally:
        db_conn.close()

    if not data:
        raise ValueError(
            f"No SC852 test data found for environment: {ENVIRONMENT}, "
            f"condition: {condition}"
        )

    client_number = str(data[2]).strip()
    ird_number = str(data[3]).strip()
    user_id = str(data[4]).strip()
    template_code = str(data[5]).strip()

    return {
        "request_body": payloads.sc852.get_payload_sc852(
            client_number=client_number,
            ird_number=ird_number,
            user_id=user_id,
            template_code=template_code,
        ),
        "header": payloads.sc852.get_headers_sc852(),
        "condition": condition,
    }

def sc835_payload_setup(condition="successful_response"):
    db = SqliteConnection()
    db.connect()

    try:
        data = db.get_data(
            table_name="SC835", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC835 test data was found for condition: {condition}")
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = CLIENT_NUMBER
    # 3 = TEMPLATE_CODE
    # 4 = SECURITY_TOKEN_ID
    client_number = data[2]
    template_code = data[3]
    security_token_id = data[4]

    return {
        "request_body": payloads.sc835.get_payload_sc835(
            client_number=client_number, template_code=template_code, security_token_id=security_token_id
        ),
        "header": payloads.sc835.get_headers_sc835()
    }


def sc890_payload_setup(condition="grant_assistance_failed"):
    nz_timezone = ZoneInfo("Pacific/Auckland")

    request_date_time = datetime.now(nz_timezone).isoformat(timespec="seconds")

    if condition in {"grant_assistance_failed", "client_not_recognised"}:
        db_conn = SqliteConnection()
        db_conn.connect()

        try:
            data = db_conn.get_data(
                table_name="SC890", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
            )
        finally:
            db_conn.close()

        if not data:
            raise ValueError(f"No SC890 test data found for {condition}")

        client_number = str(data[2]).zfill(9)
        application_date = str(data[3])
        account = str(data[4]).zfill(7)

    else:
        raise ValueError(f"Unsupported SC890 condition: {condition}")

    return {
        "request_body": payloads.sc890.get_payload_sc890(
            client_number=client_number,
            application_date=application_date,
            request_date_time=request_date_time,
            account=account
        ),
        "header": payloads.sc890.get_headers_sc890(),
        "condition": condition,
        "client_number": client_number,
        "application_date": application_date
    }


def sc346_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data("SC346", {"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition})
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC346 test data found for environment: {ENVIRONMENT}, condition: {condition}")

    # SC346 table:
    # 0 = ENVIRONMENT
    # 1 = CONDITION
    # 2 = ACTION
    # 3 = PROVIDER_ID
    # 4 = VACANCY_REFERENCE

    action = str(data[2]).strip()
    provider_id = str(data[3]).strip()
    vacancy_reference = str(data[4]).strip()

    return {
        "request_body": payloads.sc346.get_payload_sc346(
            action=action, provider_id=provider_id, vacancy_reference=vacancy_reference
        ),
        "header": payloads.sc346.get_headers_sc346(),
        "condition": condition,
        "raise_error": True
    }


def dpint453_payload_setup(condition: str = None, method: str = None, previous_doc_id: str = None):
    headers = payloads.dpint453.dpint453_headers(method=method)
    body = payloads.dpint453.get_dpint453_form_data()
    document = payloads.dpint453.get_dpint453_file()
    if condition == "delete_successful":
        db_conn = SqliteConnection()
        db_conn.connect()
        try:
            data = db_conn.get_data("DPINT453", {"ENV": ENVIRONMENT, "CONDITION": condition})
            for i in range(10):
                if data[1] == previous_doc_id:
                    data = db_conn.get_data("DPINT453", {"ENV": ENVIRONMENT, "CONDITION": condition})
                else:
                    break
        finally:
            db_conn.close()
        params = payloads.dpint453.dpint453_params(data[1])
    else:
        params = payloads.dpint453.dpint453_params()

    return headers, body, document, params


def dp595_payload_setup():
    headers = payloads.dp595.dp595_headers()
    return headers


def sc595_payload_setup():
    headers = payloads.sc595.sc595_headers()
    return headers


def sc809_payload_setup(condition="successful_transaction"):
    db = SqliteConnection()
    db.connect()

    try:
        scenario_data = db.get_data(
            table_name="SC809", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db.close()

    if not scenario_data:
        raise ValueError(f"No SC809 test data was found for ENVIRONMENT={ENVIRONMENT}, CONDITION={condition}")

    client_number = str(scenario_data[2]).zfill(9)

    return {
        "request_body": payloads.sc809.get_payload_sc809(client_number=client_number),
        "header": payloads.sc809.get_headers_sc809(),
        "client_number": client_number,
        "condition": condition
    }


def sc934_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(
            table_name="SC934", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC934 test data found for environment: {ENVIRONMENT}, condition: {condition}")

    return {
        "header": payloads.sc934.get_headers_sc934(),
        "campaign_name": str(data[2]),
        "condition": condition,
        "raise_on_error": condition != "invalid_request"
    }


def sc935_payload_setup(condition="successful_transaction"):
    db_conn = SqliteConnection()
    db_conn.connect()

    try:
        data = db_conn.get_data(
            table_name="SC935", column_names_and_values={"ENVIRONMENT": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db_conn.close()

    if not data:
        raise ValueError(f"No SC935 test data found for environment: {ENVIRONMENT}, condition: {condition}")

    campaign_name = str(data[2])

    return {
        "header": payloads.sc935.get_headers_sc935(),
        "campaign_name": campaign_name,
        "condition": condition,
        "raise_on_error": condition != "invalid_request"
    }


def sc162_payload_setup(condition="successful_transaction"):
    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "SC162.csv"

    test_data = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row["ENVIRONMENT"].strip() == ENVIRONMENT and row["CONDITION"].strip() == condition:
                test_data = row
                break

    if test_data is None:
        raise ValueError(f"No SC162 test data found for environment: {ENVIRONMENT}, condition: {condition}")

    participant_id = str(test_data["PARTICIPANT_ID"]).zfill(9)

    return {
        "participant_id": participant_id,
        "request_body": payloads.sc162.get_payload_sc162(
            report_job_search_id=str(test_data["REPORT_JOB_SEARCH_ID"]),
            activity_id=str(test_data["ACTIVITY_ID"]),
            week_code=test_data["WEEK_CODE"],
            activity_type=test_data["ACTIVITY_TYPE"]
        ),
        "header": payloads.sc162.get_headers_sc162(),
        "condition": condition,
        "raise_error": condition == "successful_transaction"
    }


def dp162_payload_setup(condition="successful_transaction"):
    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "DP162.csv"

    test_data = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row["CONDITION"].strip() == condition:
                test_data = row
                break

    if test_data is None:
        raise ValueError(f"No DP162 test data found for condition: {condition}")

    participant_id = str(test_data["PARTICIPANT_ID"]).zfill(9)

    return {
        "participant_id": participant_id,
        "request_body": payloads.dp162.get_payload_dp162(
            report_job_search_id=str(test_data["REPORT_JOB_SEARCH_ID"]),
            activity_id=str(test_data["ACTIVITY_ID"]),
            week_code=test_data["WEEK_CODE"],
            activity_type=test_data["ACTIVITY_TYPE"]
        ),
        "header": payloads.dp162.get_headers_dp162(condition),
        "condition": condition,
        "raise_error": condition == "successful_transaction"
    }


def _generate_int097_name():
    suffix = "".join(random.choices(string.ascii_uppercase, k=6))

    return f"Test{suffix}", f"Auto{suffix}"


def _get_available_int097_irds(count):
    db = SqliteConnection()
    db.connect()

    try:
        db.cur.execute(
            """
            SELECT IRD_NUMBER
            FROM INT097_IRD
            WHERE ENVIRONMENT = ?
            LIMIT ?
            """,
            ("dev11", count)
        )

        results = db.cur.fetchall()

        if len(results) < count:
            raise ValueError(f"INT097 requires {count} available IRD number(s)")

        irds = [str(row[0]).zfill(9) for row in results]

        for ird_number in irds:
            db.cur.execute(
                """
                DELETE FROM INT097_IRD
                WHERE ENVIRONMENT = ?
                AND IRD_NUMBER = ?
                """,
                ("dev11", ird_number)
            )

        db.cur.connection.commit()

        return irds

    finally:
        db.close()


def int097_payload_setup(condition="successful_transaction"):
    db = SqliteConnection()
    db.connect()

    try:
        data = db.get_data(
            table_name="INT097", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition}
        )
    finally:
        db.close()

    if not data:
        raise ValueError(f"No INT097 test data found for condition: {condition}")

    # INT097.csv values
    partner_swn = data[2]
    middle_name = data[3]
    date_of_birth = data[4]
    gender = data[5]
    ethnicity = data[6]
    ird_number = data[7]
    country_of_birth = data[8]
    marital_status = data[9]
    marital_status_date = data[10]
    address_line1 = data[11]
    address_line2 = data[12]
    suburb = data[13]
    city = data[14]
    residency_status = data[15]
    residency_status_change_date = data[16]

    # Positive scenario
    if condition == "successful_transaction":
        iib_ird, azure_ird = _get_available_int097_irds(2)

        iib_first_name, iib_family_name = _generate_int097_name()
        azure_first_name, azure_family_name = _generate_int097_name()

        return {
            "iib_request_body": payloads.int097.get_payload_int097(
                partner_swn=partner_swn,
                family_name=iib_family_name,
                first_name=iib_first_name,
                middle_name=middle_name,
                date_of_birth=date_of_birth,
                gender=gender,
                ethnicity=ethnicity,
                ird_number=iib_ird,
                country_of_birth=country_of_birth,
                marital_status=marital_status,
                marital_status_date=marital_status_date,
                address_line1=address_line1,
                address_line2=address_line2,
                suburb=suburb,
                city=city,
                residency_status=residency_status,
                residency_status_change_date=residency_status_change_date
            ),
            "azure_request_body": payloads.int097.get_payload_int097(
                partner_swn=partner_swn,
                family_name=azure_family_name,
                first_name=azure_first_name,
                middle_name=middle_name,
                date_of_birth=date_of_birth,
                gender=gender,
                ethnicity=ethnicity,
                ird_number=azure_ird,
                country_of_birth=country_of_birth,
                marital_status=marital_status,
                marital_status_date=marital_status_date,
                address_line1=address_line1,
                address_line2=address_line2,
                suburb=suburb,
                city=city,
                residency_status=residency_status,
                residency_status_change_date=residency_status_change_date
            ),
            "header": payloads.int097.get_headers_int097(),
            "condition": condition,
            "iib_ird": iib_ird,
            "azure_ird": azure_ird
        }

    # Negative scenarios
    first_name, family_name = _generate_int097_name()

    return {
        "request_body": payloads.int097.get_payload_int097(
            partner_swn=partner_swn,
            family_name=family_name,
            first_name=first_name,
            middle_name=middle_name,
            date_of_birth=date_of_birth,
            gender=gender,
            ethnicity=ethnicity,
            ird_number=ird_number,
            country_of_birth=country_of_birth,
            marital_status=marital_status,
            marital_status_date=marital_status_date,
            address_line1=address_line1,
            address_line2=address_line2,
            suburb=suburb,
            city=city,
            residency_status=residency_status,
            residency_status_change_date=residency_status_change_date
        ),
        "header": payloads.int097.get_headers_int097(),
        "condition": condition
    }


def sc526_payload_setup(condition="successful_transaction"):
    db = SqliteConnection()
    db.connect()

    try:
        data = db.get_data(table_name="SC526", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition})
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC526 test data found for condition: {condition}")

    client_number = data[2]
    start_date = data[3]
    end_date = data[4]

    return {
        "request_body": payloads.sc526.get_payload_sc526(
            condition=condition, client_number=client_number, start_date=start_date, end_date=end_date
        ),
        "header": payloads.sc526.get_headers_sc526(),
        "condition": condition
    }


def sc931_payload_setup(condition: str = None):
    headers = payloads.sc931.get_headers_sc931()
    body = payloads.sc931.get_payload_sc931()
    if condition == "invalid_request":
        body["action"] = "bob"
    elif condition == "update":
        body["action"] = "update"
        body["ocsRecord"]["weight"] = 5
    elif condition == "cancel":
        body["action"] = "cancelrecord"
    elif condition == "authentication_failure":
        del headers["Authorization"]

    return headers, body


def sc152_payload_setup(condition="successful_transaction"):
    """
    SC152 POST/Create Job Search Activity request.
    """

    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "SC152.csv"

    test_data = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row["ENVIRONMENT"].strip() == ENVIRONMENT and row["CONDITION"].strip() == condition:
                test_data = row
                break

    if test_data is None:
        raise ValueError(f"No SC152 POST test data found for environment: {ENVIRONMENT}, condition: {condition}")

    action_id = str(test_data["ACTION_ID"]).strip()

    return {
        "action_id": action_id,
        "request_body": payloads.sc152.get_payload_sc152(
            action_id=action_id,
            application_date=test_data["APPLICATION_DATE"],
            employer_name=test_data["EMPLOYER_NAME"],
            role_applied=test_data["ROLE_APPLIED"],
            application_method=test_data["APPLICATION_METHOD"],
            other_application_method=test_data["OTHER_APPLICATION_METHOD"],
            application_status=test_data["APPLICATION_STATUS"]
        ),
        "header": payloads.sc152.get_headers_sc152(operation="POST"),
        "condition": condition,
        "raise_error": (condition == "successful_transaction")
    }


def sc152_update_payload_setup(condition="successful_update"):
    """
    SC152 PUT/Update Job Search Activity request.
    """

    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "SC152.csv"

    test_data = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row["ENVIRONMENT"].strip() == ENVIRONMENT and row["CONDITION"].strip() == condition:
                test_data = row
                break

    if test_data is None:
        raise ValueError(f"No SC152 PUT test data found for environment: {ENVIRONMENT}, condition: {condition}")

    action_id = str(test_data["ACTION_ID"]).strip()

    job_search_activity_id = str(test_data["JOB_SEARCH_ACTIVITY_ID"]).strip()

    return {
        "action_id": action_id,
        "job_search_activity_id": job_search_activity_id,
        "request_body": payloads.sc152.get_update_payload_sc152(
            action_id=action_id,
            job_search_activity_id=job_search_activity_id,
            application_status=test_data["APPLICATION_STATUS"]
        ),
        "header": payloads.sc152.get_headers_sc152(operation="PUT"),
        "condition": condition,
        "raise_error": (condition == "successful_update")
    }


def dp152_payload_setup(condition="successful_transaction"):
    """Prepare DP152 POST request using DP152.csv."""
    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "DP152.csv"

    test_data = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            if row["ENVIRONMENT"].strip() == ENVIRONMENT and row["CONDITION"].strip() == condition:
                test_data = row
                break

    if test_data is None:
        raise ValueError(f"No DP152 POST test data found for environment: {ENVIRONMENT}, condition: {condition}")

    action_id = test_data["ACTION_ID"].strip()

    return {
        "action_id": action_id,
        "request_body": payloads.dp152.get_payload_dp152(
            action_id=action_id,
            application_date=test_data["APPLICATION_DATE"],
            employer_name=test_data["EMPLOYER_NAME"],
            role_applied=test_data["ROLE_APPLIED"],
            application_method=test_data["APPLICATION_METHOD"],
            other_application_method=test_data["OTHER_APPLICATION_METHOD"],
            application_status=test_data["APPLICATION_STATUS"]
        ),
        "header": payloads.dp152.get_headers_dp152(operation="POST"),
        "condition": condition,
        "raise_error": condition == "successful_transaction"
    }


def dp152_update_payload_setup(condition="successful_update"):
    """Prepare DP152 PUT request using DP152.csv."""
    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "DP152.csv"

    test_data = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            if row["ENVIRONMENT"].strip() == ENVIRONMENT and row["CONDITION"].strip() == condition:
                test_data = row
                break

    if test_data is None:
        raise ValueError(f"No DP152 PUT test data found for environment: {ENVIRONMENT}, condition: {condition}")

    action_id = test_data["ACTION_ID"].strip()
    job_search_activity_id = test_data["JOB_SEARCH_ACTIVITY_ID"].strip()

    return {
        "action_id": action_id,
        "job_search_activity_id": job_search_activity_id,
        "request_body": payloads.dp152.get_update_payload_dp152(
            action_id=action_id,
            job_search_activity_id=job_search_activity_id,
            application_status=test_data["APPLICATION_STATUS"]
        ),
        "header": payloads.dp152.get_headers_dp152(operation="PUT"),
        "condition": condition,
        "raise_error": condition == "successful_update"
    }


def sc127_payload_setup(condition="successful_transaction"):
    db = SqliteConnection()
    db.connect()

    try:
        data = db.get_data(table_name="SC127", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition})
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC127 test data found for condition: {condition}")

    client_number = data[2]

    return {
        "request_body": payloads.sc127.get_payload_sc127(client_number=client_number),
        "header": payloads.sc127.get_headers_sc127(),
        "client_number": client_number,
        "condition": condition
    }


def dp127_payload_setup(condition="successful_transaction"):
    db = SqliteConnection()
    db.connect()

    try:
        data = db.get_data(table_name="SC127", column_names_and_values={"ENVIRONMENT": "dev11", "CONDITION": condition})
    finally:
        db.close()

    if not data:
        raise ValueError(f"No SC127 test data found for condition: {condition}")

    client_number = str(data[2]).zfill(9)

    return {
        "header": payloads.dp127.get_headers_dp127(),
        "params": payloads.dp127.get_params_dp127(client_number=client_number),
        "condition": condition,
        "client_number": client_number
    }

def sc1000_payload_setup(condition: str = None):
    headers = payloads.sc1000.get_headers_sc1000()
    params = payloads.sc1000.get_params_sc1000()
    db_conn = SqliteConnection()
    db_conn.connect()
    try:
        client = db_conn.get_data(
            table_name="SC1000", column_names_and_values={"ENV": ENVIRONMENT, "CONDITION": condition}
        )
    finally:
        db_conn.close()

    return headers, params, client


def sc843_payload_setup(condition="successful_transaction"):
    csv_path = Path(__file__).resolve().parents[3] / "service_contract_data" / "SC843.csv"

    test_data = None

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if row["ENVIRONMENT"].strip() == ENVIRONMENT and row["CONDITION"].strip() == condition:
                test_data = row
                break

    if test_data is None:
        raise ValueError(f"No SC843 test data found for environment: {ENVIRONMENT}, condition: {condition}")

    return {
        "request_body": payloads.sc843.get_payload_sc843(
            region=test_data["REGION"].strip(), city=test_data["CITY"].strip(), suburb=test_data["SUBURB"].strip()
        ),
        "header": payloads.sc843.get_headers_sc843(),
        "condition": condition,
        "raise_error": False
    }

def sc840_payload_setup(condition: str = None):
    headers = payloads.sc840.sc840_headers()
    body = payloads.sc840.sc840_body()

    if condition == "no_matching_record":
        body = replace_tag_value(body, "line1", "2466B Tinakori Road")
    elif condition == "invalid_search":
        body = replace_tag_value(body, "formatType", "NZPOSTFORMATTED")

    return headers, body

def dp840_payload_setup(condition: str = None):
    headers = payloads.dp840.dp840_headers()
    city, suburb, address_line2, address_line1 = "Wellington", "Thorndon", "Thorndon", "246B Tinakori Road"

    if condition == "no_matching_record":
        params = payloads.dp840.dp840_params(city=city, suburb=suburb, address_line2=address_line2,
                                             address_line1="2466B Tinakori Road")
    else:
        params = payloads.dp840.dp840_params(city=city, suburb=suburb, address_line2=address_line2,
                                             address_line1=address_line1)

    return headers, params
