import logging
import sqlite3
from pathlib import Path

"""The .db file can be opened with https://sqliteviewer.app/#/ to view data/tables"""


class SqliteConnection:
    def __init__(self, db_name: str = "Service_contract_data.db"):
        self.root = Path(__file__).resolve().parents[2]
        self._db_name = str(self.root / db_name)
        self.connection = None
        self.cur = None

    def find_db(self):
        db_path = next(self.root.rglob(Path(self._db_name).name), None)
        if db_path is None:
            raise FileNotFoundError("Service_contract_data.db not found")
        else:
            logging.info(f"Found {db_path}")
        return db_path

    def connect(self):
        db_path = self.find_db()
        logging.info(f"Connecting to DB location located at: {db_path}")
        self.connection = sqlite3.connect(str(db_path))
        self.cur = self.connection.cursor()
        return self.connection

    def close(self):
        logging.info("Closing SQLite connection.")
        self.cur.close()
        self.connection.close()

    def get_data(self, table_name: str, column_names_and_values: dict):
        """Used to retrieve data from the SQLite database Service_contract_data.db
        Args:
            table_name (str): name of the SQLite table to pull data from
            column_names_and_values (dict): the columns and values used to determine the correct data
        """
        keys = list(column_names_and_values.keys())
        values = list(column_names_and_values.values())
        all_values = None
        try:
            for i in range(len(keys)):
                if all_values is None:
                    all_values = f"{keys[i]}='{values[i]}'"
                else:
                    all_values = f"{all_values} AND {keys[i]}='{values[i]}'"

            query = f"SELECT * FROM {table_name} WHERE {all_values} ORDER BY RANDOM() LIMIT 1;"
            self.cur.execute(query)
            results = self.cur.fetchall()
            return results[0]
        except Exception as e:
            logging.info(f"Failure while trying to retrieve data from {table_name}, failed with error: {e}")

    def insert_data(self, table_name: str, data: list[str]):
        """Used to insert data into the SQLite database Service_contract_data.db
        Args:
            table_name (str): name of the SQLite table to insert the data into
            data (list): a list of values to be inserted into the SQLite table,
        NOTE:
            make sure the data list are listed in the same way as they are displayed in the db table
        """
        query = f"INSERT INTO {table_name} VALUES ({data})".strip("[]").replace("]", "").replace("[", "")
        self.cur.execute(query)
        self.cur.connection.commit()

    def delete_data(self, table_name: str, data_identifier: dict):
        """Used to delete data from the SQLite database Service_contract_data.db
        NOTE:
            THIS CANNOT BE UNDONE!!!
        Args:
            table_name (str): name of the SQLite table to delete data from
            data_identifier (dict): the columns and values used to determine the correct set of data to delete
        """
        keys = list(data_identifier.keys())
        values = list(data_identifier.values())
        all_values = None

        for i in range(len(keys)):
            if all_values is None:
                all_values = f"{keys[i]}='{values[i]}'"
            else:
                all_values = f"{all_values} AND {keys[i]}='{values[i]}'"

        query = f"DELETE FROM {table_name} WHERE {all_values}"
        self.cur.execute(query)
        self.cur.connection.commit()

    def update_data(self, table_name: str, data_identifier: dict, new_data: dict):
        """Used to update table data in the SQLite database Service_contract_data.db"""
        id_keys = list(data_identifier.keys())
        id_values = list(data_identifier.values())
        all_id_values = None
        for i in range(len(id_keys)):
            if all_id_values is None:
                all_id_values = f"{id_keys[i]}='{id_values[i]}'"
            else:
                all_id_values = f"{all_id_values} AND {id_keys[i]}='{id_values[i]}'"

        new_data_keys = list(new_data.keys())
        new_data_values = list(new_data.values())
        all_new_data_values = None
        for i in range(len(new_data_keys)):
            if all_new_data_values is None:
                all_new_data_values = f"{new_data_keys[i]}='{new_data_values[i]}'"
            else:
                all_new_data_values = f"{all_new_data_values}, {new_data_keys[i]}='{new_data_values[i]}'"

        query = f"UPDATE {table_name} SET {all_new_data_values} WHERE {all_id_values};"
        self.cur.execute(query)
        self.cur.connection.commit()

    def create_table(self, table_name: str, table_columns: list[str], table_column_types: list[str]):
        """Used to create a new table in the SQLite database Service_contract_data.db
        Args:
            table_name (str): name the new table will be called
            table_columns (list(str)): a list of names for each column that will be created within the table
            table_column_types (list(str)): what type of data the columns expect. e.g. TEXT, INT/INTEGER
        """
        all_columns = None
        for i in range(len(table_columns)):
            if all_columns is None:
                all_columns = f"'{table_columns[i]}' '{table_column_types[i]}', "
            elif i == len(table_columns) - 1:
                all_columns = f"{all_columns} '{table_columns[i]}' '{table_column_types[i]}'"
            else:
                all_columns = f"{all_columns} '{table_columns[i]}' '{table_column_types[i]}', "

        query = f"CREATE TABLE {table_name}({all_columns});"
        self.cur.connection.execute(query)
        self.cur.connection.commit()

    def delete_table(self, table_name: str):
        """Used to delete a table in the SQLite database Service_contract_data.db
        NOTE:
            THIS CANNOT BE UNDONE!!!
        Args:
            table_name (str): name of the table to delete
        """
        query = f"DROP TABLE {table_name}"
        self.cur.connection.execute(query)
        self.cur.connection.commit()


def test_merge_databases():
    import glob
    import sqlite3
    from pathlib import Path

    master_db = Path(__file__).resolve().parents[2] / "Service_contract_data.db"

    with sqlite3.connect(master_db) as master_conn:
        cursor = master_conn.cursor()

        for filepath in glob.glob(r"C:/NotBackedUp/backups/*.db"):
            print(f"\nProcessing: {filepath}")

            cursor.execute(f"ATTACH DATABASE '{filepath}' AS repo")

            try:
                cursor.execute("""
                    SELECT name, sql
                    FROM repo.sqlite_master
                    WHERE type = 'table'
                    AND name NOT LIKE 'sqlite_%'
                """)
                repo_tables = cursor.fetchall()

                for table_name, create_sql in repo_tables:
                    # Create table if missing
                    cursor.execute(
                        """
                        SELECT 1
                        FROM main.sqlite_master
                        WHERE type = 'table'
                        AND name = ?
                    """,
                        (table_name,)
                    )

                    if cursor.fetchone() is None:
                        cursor.execute(create_sql)
                        print(f"Created table: {table_name}")

                    # Get column information
                    cursor.execute(f'PRAGMA repo.table_info("{table_name}")')
                    table_info = cursor.fetchall()

                    if not table_info:
                        continue

                    columns = [row[1] for row in table_info]
                    column_list = ", ".join(f'"{c}"' for c in columns)

                    # check if the table has a PK or UNIQUE constraint/index
                    has_pk = any(row[5] > 0 for row in table_info)

                    cursor.execute(f'PRAGMA repo.index_list("{table_name}")')
                    indexes = cursor.fetchall()

                    has_unique = any(idx[2] == 1 for idx in indexes)

                    # Tables with PK/UNIQUE:
                    #     overwrite existing rows
                    #
                    # Tables without PK/UNIQUE:
                    #     insert only rows that don't already exist

                    if has_pk or has_unique:
                        cursor.execute(f"""
                            INSERT OR REPLACE INTO main."{table_name}"
                            ({column_list})
                            SELECT {column_list}
                            FROM repo."{table_name}";
                        """)

                        print(f"Merged (REPLACE): {table_name}")

                    else:
                        match_clause = " AND ".join([f'm."{c}" IS r."{c}"' for c in columns])

                        cursor.execute(f"""
                            INSERT INTO main."{table_name}"
                            ({column_list})
                            SELECT {column_list}
                            FROM repo."{table_name}" r
                            WHERE NOT EXISTS (
                                SELECT 1
                                FROM main."{table_name}" m
                                WHERE {match_clause}
                            );
                        """)

                        print(f"Merged (DEDUPE): {table_name}")

                master_conn.commit()

            finally:
                cursor.execute("DETACH DATABASE repo")

    print("\nAll repositories merged successfully.")


# def test_get_data():
#     db = SqliteConnection()
#     db.connect()
#     identifier = {"ENV": "dev11", "Notification_created": "FALSE"}
#     print(db.get_data(table_name="sc829", column_names_and_values=identifier))


# def test_create_table():
#     db = SqliteConnection()
#     db.connect()
#     table_columns = ["ENV", "SWN", "CONDITION"]
#     table_column_types = ["TEXT", "TEXT", "TEXT"]
#     db.create_table("SC1000", table_columns, table_column_types)
#
#
# def test_add_data():
#     db = SqliteConnection()
#     db.connect()
#     data = [
#         ["dev11", "520810900", "transaction_successful"],
#     ]
#     for i in range(len(data)):
#         db.insert_data("SC1000", data[i])

# def test_delete():
#     db = SqliteConnection()
#     db.connect()
#     db.delete_table(table_name="SC863")

# def test_update_db():
#     db = SqliteConnection()
#     db.connect()
#     identifier = {"CONDITION": "schema_validation"}
#     new_data = {"card_no": "5O35137O3O8O3O51"}
#     db.update_data(table_name="SC510", data_identifier=identifier, new_data=new_data)


# def test_delete_data():
#     db = SqliteConnection()
#     db.connect()
#     identifier = {"SERVICE_CONTRACT": "SC511"}
#     db.delete_data(table_name="ENDPOINTS", data_identifier=identifier)
