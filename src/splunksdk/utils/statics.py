"""Static Properties."""

from typing import List

ENCODING = "utf-8"
KVSTORE_QUERY: List[str] = ["sort", "limit", "skip", "fields"]
SPLUNK_OUTPUTMODES: List[str] = ["xml", "json", "json_cols", "json_rows", "csv", "atom", "raw"]
