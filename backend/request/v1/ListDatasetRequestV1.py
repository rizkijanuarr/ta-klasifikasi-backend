from dataclasses import dataclass
from typing import Optional

@dataclass
class ListDatasetRequestV1:
    is_legal: int
    limit_data: int
    page: Optional[int] = 1  # Default page 1

    def __post_init__(self):
        # is_legal can be 0 or 1, so check for None instead
        if self.is_legal is None:
            raise ValueError("is_legal is required")
        if self.is_legal not in [0, 1]:
            raise ValueError("is_legal must be 0 or 1")

        if not self.limit_data or self.limit_data <= 0:
            raise ValueError("limit_data must be greater than 0")
        if self.limit_data > 1000:
            raise ValueError("limit_data cannot exceed 1000")

        # Validate page
        if self.page is None or self.page <= 0:
            self.page = 1  # Default to page 1
