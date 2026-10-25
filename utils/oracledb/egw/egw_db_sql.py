import logging
import pytest
from default_config import ENVIRONMENT, EXTERNAL_DB
from utils.oracledb.OracleConnector import db_connector
from utils.oracledb.egw.queries.queries import get_query


def get_egw_connection():
    if not EXTERNAL_DB:
        raise Exception(
            "EGW_TEST environment variable is set to false therefore Payment Cards cannot be retrieved "
            "from the mock EGW database"
        )
    else:
        connection_string = pytest.auto_db_env_parameters["EftPosGatewayCards_Host"]
        user = pytest.auto_db_env_parameters["EftPosGatewayCardsDBUser"]
        # if ENVIRONMENT[0].lower() == 'u':
        #     password = get_pass(pytest.auto_db_env_parameters["EftPosGatewayCardsDBPwd"])
        # else:
        password = pytest.auto_db_env_parameters["EftPosGatewayCardsDBPwd"]
        return user + "/" + password + "@" + connection_string


@db_connector
def insert(cnn, insert_query, args):
    cur = cnn.cursor()
    cur.execute(insert_query, args)


@db_connector
def get_payment_card_number(cnn):
    sql_statement = get_query(option="get")
    cur = cnn.cursor()
    query_result = cur.execute(sql_statement)
    for result in query_result:
        next_valid_card_number = result[0]
        logging.info("Next valid card number: " + next_valid_card_number)
        return next_valid_card_number


def get_next_pc_insert_into_db() -> str:
    conn = get_egw_connection()
    number = get_payment_card_number(conn)
    query = get_query(option="insert")
    insert(conn, query, [f"pc-{number}", number])
    return number


def test_db():
    get_next_pc_insert_into_db()
