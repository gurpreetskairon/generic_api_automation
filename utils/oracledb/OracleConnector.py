import logging

import oracledb


class OracleConnection:
    def __init__(self, connection_string=None):
        if connection_string is None:
            raise ValueError("Must provide a connection string")
        auth = connection_string
        logging.info("auth: %s", auth)
        oracledb.init_oracle_client()
        self.connection = oracledb.connect(auth)

    def connect(self):
        return self.connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def db_connector(func):
    def with_connection_(conn_str, *args, **kwargs):
        cnn = oracledb.connect(conn_str)
        try:
            rv = func(cnn, *args, **kwargs)
        except oracledb.DatabaseError as e:
            cnn.rollback()
            logging.critical("Oracle DB error: %s", e)
            raise
        else:
            cnn.commit()
        finally:
            cnn.close()
        return rv

    return with_connection_
