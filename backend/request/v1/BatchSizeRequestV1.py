from dataclasses import dataclass
from typing import Optional, List


@dataclass
class BatchSizeRequestV1:
    """
    Request DTO untuk Batch Size Evaluation

    Attributes:
        is_legal (Optional[int]): Filter data berdasarkan kategori
            - 0 = Illegal only
            - 1 = Legal only
            - None = Semua data (ILLEGAL + LEGAL)
        batch_sizes (Optional[List[int]]): List of batch sizes to test
            - Default: [8, 16, 32, 64, 128, 256]
            - Minimum: 1
            - Maximum: total dataset size
    """
    is_legal: Optional[int] = None
    batch_sizes: Optional[List[int]] = None

    def __post_init__(self):
        """Validate request parameters"""

        # Validate is_legal
        if self.is_legal is not None:
            if not isinstance(self.is_legal, int):
                raise ValueError("is_legal must be an integer (0 or 1)")
            if self.is_legal not in [0, 1]:
                raise ValueError("is_legal must be 0 (ILLEGAL) or 1 (LEGAL)")

        # Set default batch_sizes if not provided
        if self.batch_sizes is None:
            self.batch_sizes = [8, 16, 32, 64, 128, 256]

        # Validate batch_sizes
        if not isinstance(self.batch_sizes, list):
            raise ValueError("batch_sizes must be a list of integers")

        if len(self.batch_sizes) == 0:
            raise ValueError("batch_sizes must contain at least one value")

        if len(self.batch_sizes) > 10:
            raise ValueError("batch_sizes cannot contain more than 10 values")

        # Validate each batch size
        for batch_size in self.batch_sizes:
            if not isinstance(batch_size, int):
                raise ValueError(f"batch_size must be an integer, got {type(batch_size)}")

            if batch_size < 1:
                raise ValueError(f"batch_size must be at least 1, got {batch_size}")

            if batch_size > 10000:
                raise ValueError(f"batch_size cannot exceed 10000, got {batch_size}")

        # Remove duplicates and sort
        self.batch_sizes = sorted(list(set(self.batch_sizes)))
