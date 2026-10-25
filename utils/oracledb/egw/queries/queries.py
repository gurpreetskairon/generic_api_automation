from pathlib import Path
from typing import Literal

get_payment_card = Path("utils/oracledb/egw/queries/get_payment_card_number.sql")
insert_payment_card = Path("utils/oracledb/egw/queries/insert_payment_card.sql")


def _read_file(file_location):
    file = open(file_location)
    query = file.read()
    file.close()
    return query


def get_query(option: Literal["get", "insert"]):
    if option == "get":
        return _read_file(get_payment_card)
    elif option == "insert":
        return _read_file(insert_payment_card)
