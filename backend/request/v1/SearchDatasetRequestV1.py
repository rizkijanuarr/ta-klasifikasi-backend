from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchDatasetRequestV1:
    search_query: str
    is_legal: Optional[int] = None  # Optional filter by is_legal (0 or 1)
    limit_data: int = 10
    page: Optional[int] = 1

    def __post_init__(self):
        # Validate search_query
        if not self.search_query or not self.search_query.strip():
            raise ValueError("search_query is required and cannot be empty")

        # Validate is_legal if provided
        if self.is_legal is not None and self.is_legal not in [0, 1]:
            raise ValueError("is_legal must be 0 or 1")

        # Validate limit_data
        if not self.limit_data or self.limit_data <= 0:
            raise ValueError("limit_data must be greater than 0")
        if self.limit_data > 1000:
            raise ValueError("limit_data cannot exceed 1000")

        # Validate page
        if self.page is None or self.page <= 0:
            self.page = 1  # Default to page 1
