import os
import uuid

from utils.helpers.dynamic_tokens import register_token


@register_token("generate_uuid")
def generate_uuid(key:str=os.getenv("UUID_KEY")):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))