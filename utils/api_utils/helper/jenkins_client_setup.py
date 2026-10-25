import os
import re
import time
from html import unescape
from urllib.parse import urljoin

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_jenkins_session():
    """
    Creates a Jenkins session using environment variables.

    Required environment variables:
    - JENKINS_BASE_URL
    - JENKINS_USER
    - JENKINS_API_TOKEN
    """
    base_url = os.getenv("JENKINS_BASE_URL")
    username = os.getenv("JENKINS_USER")
    api_token = os.getenv("JENKINS_API_TOKEN")

    if not base_url:
        raise ValueError("JENKINS_BASE_URL is not set.")
    if not username:
        raise ValueError("JENKINS_USER is not set.")
    if not api_token:
        raise ValueError("JENKINS_API_TOKEN is not set.")

    session = requests.Session()
    session.auth = (username, api_token)
    session.verify = False

    return session, base_url.rstrip("/") + "/"


def trigger_client_creation_job(
    job_path: str,
    environment: str = "dev11",
    number_of_clients: int = 1,
    age: int = 27,
    swiftt_profile: str = "True",
    benefit_created_by_swiftt: str = "none",
    children: int = 0,
    use_api: str = "True",
    partner: str = "False",
    register_mymsd: str = "False",
    eos_application: str = "False"
):
    """
    Triggers the Jenkins client creation job with parameters.

    job_path example:
    job/FolderName/job/JobName/
    or
    job/Client-Creation-Job/
    """
    session, base_url = _get_jenkins_session()

    build_url = urljoin(base_url, f"{job_path.strip('/')}/buildWithParameters")

    params = {
        "Environment": environment,
        "Number_of_clients": number_of_clients,
        "Age": age,
        "Swiftt_profile": swiftt_profile,
        "Benefit_created_by_SWIFTT": benefit_created_by_swiftt,
        "Children": children,
        "use_api": use_api,
        "Partner": partner,
        "register_mymsd": register_mymsd,
        "eos_application": eos_application
    }

    response = session.post(build_url, params=params)
    response.raise_for_status()

    queue_url = response.headers.get("Location")
    if not queue_url:
        raise RuntimeError("Jenkins did not return queue location after triggering build.")

    return queue_url


def wait_for_build_number(queue_url: str, timeout_seconds: int = 120):
    """
    Waits for Jenkins queue item to become an actual build and returns build URL.
    """
    session, _ = _get_jenkins_session()

    end_time = time.time() + timeout_seconds

    while time.time() < end_time:
        response = session.get(f"{queue_url.rstrip('/')}/api/json")
        response.raise_for_status()
        queue_data = response.json()

        executable = queue_data.get("executable")
        if executable and executable.get("url"):
            return executable["url"]

        time.sleep(5)

    raise TimeoutError("Timed out waiting for Jenkins queue item to start build.")


def wait_for_build_success(build_url: str, timeout_seconds: int = 600):
    """
    Waits for Jenkins build to complete successfully.
    """
    session, _ = _get_jenkins_session()

    end_time = time.time() + timeout_seconds

    while time.time() < end_time:
        response = session.get(f"{build_url.rstrip('/')}/api/json")
        response.raise_for_status()
        build_data = response.json()

        building = build_data.get("building")
        result = build_data.get("result")

        if not building:
            if result == "SUCCESS":
                return True
            raise RuntimeError(f"Jenkins build completed with result: {result}")

        time.sleep(10)

    raise TimeoutError("Timed out waiting for Jenkins build to complete.")


def get_client_id_from_client_list(build_url: str):
    session, _ = _get_jenkins_session()

    possible_client_list_urls = [
        f"{build_url.rstrip('/')}/Client_20List/client_list.html",
        f"{build_url.rstrip('/')}/Client_20List/",
        f"{build_url.rstrip('/')}/Client_20List",
        f"{build_url.rstrip('/')}/Client_List/client_list.html",
        f"{build_url.rstrip('/')}/Client_List/",
        f"{build_url.rstrip('/')}/Client_List",
        f"{build_url.rstrip('/')}/artifact/Client_20List/client_list.html",
        f"{build_url.rstrip('/')}/artifact/client_list.html"
    ]

    last_error = None

    for index, url in enumerate(possible_client_list_urls, start=1):
        try:
            print(f"Trying Client List URL: {url}")

            response = session.get(url)
            print(f"Status code: {response.status_code}")

            if response.status_code != 200:
                continue

            html_text = unescape(response.text)

            debug_file_name = f"jenkins_client_list_debug_{index}.html"
            with open(debug_file_name, "w", encoding="utf-8") as file:
                file.write(html_text)

            print(f"Saved response to {debug_file_name}")

            # Remove HTML tags so regex can search visible text
            visible_text = re.sub(r"<[^>]+>", " ", html_text)
            visible_text = unescape(visible_text)
            visible_text = re.sub(r"\s+", " ", visible_text)

            print("Visible text preview:")
            print(visible_text[:1000])

            # Match: swn: 523456789
            match = re.search(r"\bswn\s*:\s*([0-9]{7,10})\b", visible_text, flags=re.IGNORECASE)

            if match:
                client_id = match.group(1).strip()
                print(f"Client ID found: {client_id}")
                return client_id

            print("No SWN found in this response.")

        except requests.RequestException as exc:
            last_error = exc
            print(f"Error reading Client List URL: {exc}")

    raise RuntimeError(f"Unable to extract client id from Jenkins Client List. Last error: {last_error}")


def get_client_ids_from_client_list(build_url: str):
    """
    Reads Jenkins Client List and returns all SWN/client numbers found.
    Used when Jenkins creates more than one client in the same build.
    """
    session, _ = _get_jenkins_session()

    possible_client_list_urls = [
        f"{build_url.rstrip('/')}/Client_20List/client_list.html",
        f"{build_url.rstrip('/')}/Client_20List/",
        f"{build_url.rstrip('/')}/Client_20List",
        f"{build_url.rstrip('/')}/Client_List/client_list.html",
        f"{build_url.rstrip('/')}/Client_List/",
        f"{build_url.rstrip('/')}/Client_List",
        f"{build_url.rstrip('/')}/artifact/Client_20List/client_list.html",
        f"{build_url.rstrip('/')}/artifact/client_list.html"
    ]

    last_error = None

    for index, url in enumerate(possible_client_list_urls, start=1):
        try:
            print(f"Trying Client List URL: {url}")

            response = session.get(url)
            print(f"Status code: {response.status_code}")

            if response.status_code != 200:
                continue

            html_text = unescape(response.text)

            debug_file_name = f"jenkins_client_list_debug_{index}.html"
            with open(debug_file_name, "w", encoding="utf-8") as file:
                file.write(html_text)

            visible_text = re.sub(r"<[^>]+>", " ", html_text)
            visible_text = unescape(visible_text)
            visible_text = re.sub(r"\s+", " ", visible_text)

            print("Visible text preview:")
            print(visible_text[:1000])

            client_ids = re.findall(r"\bswn\s*:\s*([0-9]{7,10})\b", visible_text, flags=re.IGNORECASE)

            client_ids = [client_id.strip() for client_id in client_ids]

            if client_ids:
                print(f"Client IDs found: {client_ids}")
                return client_ids

            print("No SWN found in this response.")

        except requests.RequestException as exc:
            last_error = exc
            print(f"Error reading Client List URL: {exc}")

    raise RuntimeError(f"Unable to extract client IDs from Jenkins Client List. Last error: {last_error}")


def create_client_using_jenkins():
    """
    Main helper used by tests.

    Required environment variables:
    - JENKINS_BASE_URL
    - JENKINS_USER
    - JENKINS_API_TOKEN
    - JENKINS_CLIENT_CREATION_JOB_PATH
    """
    job_path = os.getenv("JENKINS_CLIENT_CREATION_JOB_PATH")

    if not job_path:
        raise ValueError("JENKINS_CLIENT_CREATION_JOB_PATH is not set.")

    queue_url = trigger_client_creation_job(
        job_path=job_path,
        environment=os.getenv("JENKINS_CLIENT_ENVIRONMENT", "dev11"),
        number_of_clients=int(os.getenv("JENKINS_NUMBER_OF_CLIENTS", "1")),
        age=int(os.getenv("JENKINS_CLIENT_AGE", "27")),
        swiftt_profile=os.getenv("JENKINS_SWIFTT_PROFILE", "True"),
        benefit_created_by_swiftt=os.getenv("JENKINS_BENEFIT_CREATED_BY_SWIFTT", "none"),
        children=int(os.getenv("JENKINS_CHILDREN", "0")),
        use_api=os.getenv("JENKINS_USE_API", "True"),
        partner=os.getenv("JENKINS_PARTNER", "False"),
        register_mymsd=os.getenv("JENKINS_REGISTER_MYMSD", "False"),
        eos_application=os.getenv("JENKINS_EOS_APPLICATION", "False")
    )

    build_url = wait_for_build_number(queue_url)
    wait_for_build_success(build_url)

    client_id = get_client_id_from_client_list(build_url)

    if not client_id:
        raise RuntimeError("Jenkins build completed but no client id was found.")

    return client_id


def create_clients_using_jenkins(number_of_clients=1):
    """
    Creates one or more CMS clients using Jenkins and returns a list of client IDs.
    """
    job_path = os.getenv("JENKINS_CLIENT_CREATION_JOB_PATH")

    if not job_path:
        raise ValueError("JENKINS_CLIENT_CREATION_JOB_PATH is not set.")

    queue_url = trigger_client_creation_job(
        job_path=job_path,
        environment=os.getenv("JENKINS_CLIENT_ENVIRONMENT", "dev11"),
        number_of_clients=number_of_clients,
        age=int(os.getenv("JENKINS_CLIENT_AGE", "27")),
        swiftt_profile=os.getenv("JENKINS_SWIFTT_PROFILE", "True"),
        benefit_created_by_swiftt=os.getenv("JENKINS_BENEFIT_CREATED_BY_SWIFTT", "none"),
        children=int(os.getenv("JENKINS_CHILDREN", "0")),
        use_api=os.getenv("JENKINS_USE_API", "True"),
        partner=os.getenv("JENKINS_PARTNER", "False"),
        register_mymsd=os.getenv("JENKINS_REGISTER_MYMSD", "False"),
        eos_application=os.getenv("JENKINS_EOS_APPLICATION", "False")
    )

    build_url = wait_for_build_number(queue_url)
    wait_for_build_success(build_url)

    client_ids = get_client_ids_from_client_list(build_url)

    if not client_ids:
        raise RuntimeError("Jenkins build completed but no client IDs were found.")

    return client_ids


def create_two_clients_using_jenkins():
    """
    Creates two CMS clients using Jenkins and returns both client IDs.
    Used for SC829 comparison testing where IIB and Azure need separate fresh clients.
    """
    client_ids = create_clients_using_jenkins(number_of_clients=2)

    if len(client_ids) < 2:
        raise RuntimeError(f"Expected 2 Jenkins-created clients, but got: {client_ids}")

    return client_ids[0], client_ids[1]


def extract_client_ids_from_client_list(text):
    matches = re.findall(r"\bswn\s*:\s*([0-9]{7,10})\b", text, flags=re.IGNORECASE)

    client_ids = [client_id.strip() for client_id in matches]

    if not client_ids:
        raise RuntimeError("No SWN/client IDs found in Jenkins Client List.")

    return client_ids
