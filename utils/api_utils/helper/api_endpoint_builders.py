import logging
import os

import allure
from dotenv import load_dotenv

from apps.services.integration_api.api_content import ApiRequestDetails
from apps.services.integration_api.auth_token import AuthToken
from default_config import ENVIRONMENT, RUN_IN_SIT_ENV
from utils.sqlite.SqliteConnection import SqliteConnection


def get_endpoint_by_system(system: str, method: str = None) -> str:
    """use this function to list and retrieve the endpoint URL for API calls

    Args:
        system (str): name of the system you are wanting the api endpoint for
        method (str): what API method you are wanting for the desired system. e.g system=weka, api_type=post

    Returns:
        API endpoint
    """
    env = ""

    if len(ENVIRONMENT) >= 3:
        if "d" in ENVIRONMENT:
            env = ENVIRONMENT.replace("dev", "d")
        else:
            env = ENVIRONMENT

    endpoint = None
    if ENVIRONMENT.lower().startswith("d"):
        load_dotenv(".env.dev")
    else:
        load_dotenv(".env.uat")
    if system.lower() == "weka" and method is not None:
        if method.lower() == "get":
            endpoint = os.getenv("weka_get_endpoint")
        elif method.lower() == "post":
            endpoint = os.getenv("weka_post_end_point")
    else:
        endpoint = os.getenv(system.lower()).format(environment=env)

    if endpoint is None:
        raise Exception(f"API {method} Endpoint for system {system} not found")
    else:
        return endpoint


def setup_basic_info(
    api_request_detail_obj: ApiRequestDetails, token_data_info: dict, endpoint_system: str, api_method: str = None
):
    """
    Basic API request information setup
    Args:
        api_request_detail_obj: API Request Details Object
        token_data_info:  Token Data Information
        endpoint_system: name of the system you are wanting the endpoint for
        api_method: api method (e.g post, get etc...)
    Returns:
        None
    """
    token_data = token_data_info
    access_token = AuthToken().authenticate(token_data)
    api_request_detail_obj.headers = {"Authorization": f"{access_token}"}
    api_request_detail_obj.endpoint = get_endpoint_by_system(system=endpoint_system, method=api_method)


def build_api_endpoint(service_contract: str, system: str, sub_system: str = "NONE"):
    """
    Build an API endpoint for a specific service contract from values stored in the SQLite DB tables
    "DOMAINS" and "ENDPOINTS"

    Args:
        service_contract: name of the service contract e.g "SC825"
        system: name of the system you are wanting the api endpoint for e.g "Azure or IIB"
        sub_system: name of the subsystem you are wanting the api endpoint for e.g "STAR"
    """

    db_conn = SqliteConnection()
    db_conn.connect()
    query_names_and_values = {"ENV": ENVIRONMENT, "SYSTEM": system, "SUBSYSTEM": sub_system}
    domain = list(db_conn.get_data(table_name="DOMAINS", column_names_and_values=query_names_and_values))
    query_names_and_values = {"SERVICE_CONTRACT": service_contract, "SYSTEM": system}
    endpoint_path = db_conn.get_data(table_name="ENDPOINTS", column_names_and_values=query_names_and_values)
    if RUN_IN_SIT_ENV and domain[1] == "AZURE":
        logging.warning("Running in SIT environment")
        domain[3] = domain[3].replace("dev", "sit")
    endpoint = f"{domain[3]}{endpoint_path[2]}".replace("{ENV}", ENVIRONMENT)
    logging.info(f"Constructed Endpoint is: {endpoint}")
    allure.attach(endpoint, name="Constructed Endpoint", attachment_type=allure.attachment_type.TEXT)
    db_conn.close()
    return endpoint
