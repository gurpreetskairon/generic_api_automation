from dataclasses import dataclass
from typing import Optional


@dataclass
class LoggedResponse:
    """A response pulled out of a log system."""
    body: str
    status_code: Optional[int] = None  # None if the log entry doesn't carry one
    source: str = ""                   # "splunk" / "appinsights"


class ResponseNotFound(Exception):
    """No log entry (yet) for the given transaction id."""
