import os
import re
import uuid

from utils.helpers.dynamic_tokens import register_token


@register_token("generate_uuid")
def generate_uuid(key:str=os.getenv("UUID_KEY")):
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
    return f"{prefix[0].lower()}{number}"