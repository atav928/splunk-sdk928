"""Splunk Search Dataclasses."""

from typing import Any, Dict, List
from dataclasses import dataclass, field

from splunklib.client import Job

from pytoolkit.utilities import BaseMonitor

@dataclass
class SplunkSearchResults(BaseMonitor):
    """Splunk Search Results."""
    message: Dict[str, Any] = field(default_factory=lambda: {})
    json_response: List[Dict[str, Any]] = field(default_factory=lambda: [])

class SearchJobResults:
    """Search Job Container."""
    def __init__(self, job: Job):
        self._job_searches = [("results",job.results),("content",job.content), ("name", job.name),("search", job.search)]
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._job_searches):
            item = self._job_searches[self._index]
            self._index += 1
            return item
        raise StopIteration
        