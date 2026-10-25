import datetime
from datetime import datetime

from utils.mssql.SqlConnector import get_swiftt_environment
from utils.oracledb.OracleConnector import db_connector


def get_swiftt_connection_string():
    swiftt_env = get_swiftt_environment()
    user = str("MSD_TESTER_" + swiftt_env.upper())
    password = str("MSD_TESTER_" + swiftt_env.upper())
    connection_string = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=SWIFTT-TRACE-DB-PRT-TEST.SSI.GOVT.NZ)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=MSDSUAT1)))"
    return f"{user}/{password}@{connection_string}"


@db_connector
def get_from_swiftt(db_conn, query_file, process_results=False):
    """
    About
        Reusable function that takes a connection and query file as arguments and process them to return a result
    Args:
        db_conn: Oracle connection, pass the connection string value here
        query_file: path of the sql query to execute
        process_results: weather or not to process the results with _process_get_client_query_result()

    Returns: list
    """
    cur = db_conn.cursor()
    query = _open_file(query_file)
    query_result = cur.execute(query)
    if process_results:
        return _process_get_client_query_result(query_result)
    else:
        return query_result.fetchall()


# reusable query results processor
def _process_get_client_query_result(result):
    """
    About:
        Workflow function to process query result. Was initially handling results containing swn and dob in list
        position 0 and 1 respectively. Have amended the logic to return complete list of data retrieved from the
        query. The queries should be written in a way that returns a single row / record. swn formatting. for the
        most part is handled in this function so do not need to handle in the query
    Args:
        result: cursor object
    See Also
        _get_from_swiftt

    Returns: list
    """
    for qr in result:
        try:
            dt = datetime.date(qr[1])
            day = str(f"{dt.day:02d}")
            month = str(f"{dt.month:02d}")
            year = str(dt.year)
            return [str(f"{qr[0]:09d}"), day + "/" + month + "/" + year]
        except Exception:
            rec: list = [qr]
            return rec[0]
    raise ValueError("No data returned from the result")


def _open_file(query_file_location):
    fd = open(query_file_location)
    query = fd.read()
    fd.close()
    return query
