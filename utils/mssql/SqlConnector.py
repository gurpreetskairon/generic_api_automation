import pymssql
import pytest


class SqlConnector:
    def __init__(self):
        self.connection = pymssql.connect(
            server="sqlTosca.corp.ssi.govt.nz",
            user="AutomationUser",
            password="ApWg!D5r9pS+y[LNvkxM",
            database="TestAutomation",
            port="1433"
        )

    def connect(self):
        return self.connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_customer_details(self):
        cursor = self.connection.cursor()
        cursor.callproc("spGetNextClient", ("dev4",))
        for row in cursor:
            return row[0]

    def get_next_client_general(self, procedure_name, env):
        cursor = self.connection.cursor()
        cursor.callproc(procedure_name, (env,))
        for row in cursor:
            return row[0]

    def update_client_info(self, status, swn, result, environment):
        cursor = self.connection.cursor()
        sqlstr = (
            "update TestEnvironmentClientData set status = '"
            + status
            + "', updatetime=CURRENT_TIMESTAMP"
            + ", findckresult = '"
            + result
            + "'"
            + "where swn = '"
            + swn.lstrip("0")
            + "'"
            + " and env = '"
            + environment
            + "'"
        )
        cursor.execute(sqlstr)
        self.connection.commit()

    def insert_client_info(self, env, swn, first_name, dob):
        cursor = self.connection.cursor()
        sqlstr = (
            "insert into [TestAutomation].[dbo].[TestEnvironmentClientData] values('"
            + env
            + "','"
            + swn
            + "','"
            + first_name
            + "','"
            + dob
            + "', 'todo', 'no result', CURRENT_TIMESTAMP)"
        )
        cursor.execute(sqlstr)
        self.connection.commit()

    def delete_all_client_info(self, environment):
        cursor = self.connection.cursor()
        sqlstr = "delete from TestEnvironmentClientData where env='" + environment + "'"
        cursor.execute(sqlstr)
        self.connection.commit()

    @staticmethod
    def check_swn(swn):
        new_swn = ""
        if (9 - len(swn)) != 0:
            left = 9 - len(swn)
            for _ in range(left):
                new_swn = new_swn + "0"
            new_swn = new_swn + swn
            return new_swn
        return swn

    def get_environment_config(self, env):
        config_dict = {}
        cursor = self.connection.cursor(as_dict=True)
        sql_str = "select * from tEnvParamList where Environment = '" + env + "'"
        cursor.execute(sql_str)
        for row in cursor:
            config_dict[row["ParamName"]] = row["ParamValue"]
        return config_dict

    def check_environment_parameters(self, env, param_name):
        cursor = self.connection.cursor(as_dict=True)
        sql_str = f"""SELECT * FROM tEnvParamList  where Environment = '{env}' and ParamName = '{param_name}'"""
        cursor.execute(sql_str)
        return cursor.fetchone()

    def get_list_of_environments(self):
        results = []
        cursor = self.connection.cursor(as_dict=True)
        sql_str = """SELECT distinct(Environment) FROM tEnvParamList"""
        cursor.execute(sql_str)
        for row in cursor:
            results.append(row["Environment"])
        return results

    def get_swiftt_user(self, computer_name, swiftt_env):
        cursor = self.connection.cursor()
        cursor.callproc("spSwifttGetUser", (swiftt_env, computer_name))
        user = "notfound"
        for row in cursor:
            user = row[0]
        self.connection.commit()
        return user

    def get_authorise_swiftt_user(self, computer_name, swiftt_env):
        cursor = self.connection.cursor()
        cursor.callproc("spSwifttGetUser", (swiftt_env, f"{computer_name}A"))
        user = "notfound"
        for row in cursor:
            user = row[0]
        self.connection.commit()
        return user

    def release_swiftt_user(self, swiftt_user_id):
        # swift_env = 'SUAT' + pytest.auto_db_env_parameters["SWIFTT_TRACE_Number"]
        swift_env = get_swiftt_environment()
        cursor = self.connection.cursor()
        cursor.callproc("spSwifttSetUserLogout", (swift_env, swiftt_user_id))
        self.connection.commit()

    def release_all_swiftt_bulk_users(self):
        # swift_env = 'SUAT' + pytest.auto_db_env_parameters["SWIFTT_TRACE_Number"]
        swift_env = get_swiftt_environment()

        sql_query = f"""
        update [TestAutomation].[dbo].[tbswifttuser]
        set status='Available',
        updatetime=GETDATE(),computername=''
        where environment='{swift_env}'
                """
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        self.connection.commit()

    def release_swiftt_users_15_min_check(self):
        cursor = self.connection.cursor()
        cursor.callproc("spSwifttResetUser")
        self.connection.commit()


def get_swiftt_environment():
    swiftt_trace_number = pytest.auto_db_env_parameters["SWIFTT_TRACE_Number"]
    if str.isnumeric(swiftt_trace_number):
        swift_env = "SUAT" + swiftt_trace_number
    else:
        swift_env = swiftt_trace_number.upper()

    return swift_env
