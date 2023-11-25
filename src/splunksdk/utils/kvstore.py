"""KVStore Dataclasses."""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Collections:
    collections: List[str] = field(default_factory=lambda: [])
