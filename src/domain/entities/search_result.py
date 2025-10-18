"""SearchResult entity - Domain layer."""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SearchResult:
    """SearchResult entity representing YouTube search results."""
    
    query: str
    results_count: int
    pages_fetched: int
    results: List[Dict[str, Any]]

    def __post_init__(self):
        """Validate search result entity."""
        if not self.query:
            raise ValueError("query is required")
        if self.results_count < 0:
            raise ValueError("results_count must be non-negative")

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "query": self.query,
            "results_count": self.results_count,
            "pages_fetched": self.pages_fetched,
            "results": self.results,
        }
