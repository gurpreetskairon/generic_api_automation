import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from _pytest.nodes import Item

from default_config import PROJECT_NAME


@dataclass
class Comments:
    comment: str = ""


# noinspection PyMethodMayBeStatic
# noinspection PyUnresolvedReferences
class AllureReportConfiguration:
    def __init__(self, path: str):
        self.reusable_client_swn: str = ""
        self.reusable_client_dob: str = ""
        allure_path_root = Path(__file__).resolve().parents[2]
        self._path: str = str((allure_path_root / path.rstrip("/")) / " ").rstrip()
        self._item_info: Optional[Item] = None
        self._log_info: str = ""
        self._summary_path: str = ""
        self._html_template_path: str = "assets/summary_html/template.html"
        self._output_folder: str = "allure-results"
        self._dest_folder: str = "allure-report"
        self._history_src: str = f"{self._dest_folder}/history"
        self._history_dest: str = f"{self._output_folder}/history"

    @property
    def item_info(self) -> Optional[Item]:
        return self._item_info

    @item_info.setter
    def item_info(self, value: Item):
        self._item_info = value

    def _ensure_directory_exists(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)
        return self

    def generate_report_properties(self, browser_name: str):
        categories_data = [
            {"name": "Skipped Tests", "matchedStatuses": ["skipped"], "messageRegex": ".*"},
            {"name": "Element issue", "matchedStatuses": ["failed"], "traceRegex": ".*AttributeError.*"},
            {"name": "Product defects", "matchedStatuses": ["failed"], "messageRegex": ".*AssertionError*.*"},
            {"name": "Timeout issue", "matchedStatuses": ["failed"], "messageRegex": ".*TimeoutError.*"},
            {"name": "Framework issue", "matchedStatuses": ["failed"], "messageRegex": ".*ERR_ABORTED.*"},
            {"name": "Passed tests", "matchedStatuses": ["passed"]}
        ]
        self._ensure_directory_exists(self._path)
        env_properties = {
            "ProjectName": f"{PROJECT_NAME}",
            "Browser": browser_name,
            "System": f"{platform.system()}{platform.release()}",
            "PythonVersion": platform.python_version(),
            "Team": "Automation"
        }
        with open(f"{self._path}environment.properties", "w") as f:
            for key, value in env_properties.items():
                f.write(f"{key}={value}\n")
        with open(f"{self._path}categories.json", "w") as f:
            json.dump(categories_data, f, indent=4)
