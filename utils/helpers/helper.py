import os
import re
import uuid
<<<<<<< HEAD
from datetime import datetime
from utils.helpers.dynamic_tokens import register_token


def make_unique_string(base_string: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{base_string}_{timestamp}"

@register_token("generate_uuid")
def generate_uuid(key: str=os.getenv("UUID_KEY"), unique: bool = False) -> str:
    if key is None:
        key = os.getenv("UUID_KEY")

    if unique:
        key = make_unique_string(key)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

=======

from utils.helpers.dynamic_tokens import register_token


@register_token("generate_uuid")
def generate_uuid(key:str=os.getenv("UUID_KEY")):
>>>>>>> 6ac2d0d0 (added my generic api script code)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

@register_token("get_short_env")
def get_short_env(env_value: str=None) -> str:
    """
    Converts an environment value like 'dev11' -> 'd11', 'uat11' -> 'u11'.
    Takes the first letter of the env name + the trailing digits.
    """
    if not env_value:
        env_value = os.getenv("ENV")

    match = re.match(r"([a-zA-Z]+?)(\d+)$", env_value.strip())
    if not match:
        raise ValueError(f"Unrecognized env value format: '{env_value}'")

    prefix, number = match.groups()
<<<<<<< HEAD
    return f"{prefix[0].lower()}{number}"
=======
    return f"{prefix[0].lower()}{number}"
>>>>>>> 6ac2d0d0 (added my generic api script code)
