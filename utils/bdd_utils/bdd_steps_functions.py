import json

import allure


def attach_json_to_allure(response: dict, name: str = "API_Response"):
    allure.attach(json.dumps(response, indent=4), name=name, attachment_type=allure.attachment_type.JSON)
