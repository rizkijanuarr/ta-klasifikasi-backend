from dataclasses import dataclass
from typing import Optional, List


@dataclass
class OptimizerRequestV1:
    """
    Request DTO untuk Optimizer Comparison

    Attributes:
        is_legal (Optional[int]): Filter data berdasarkan kategori
            - 0 = Illegal only
            - 1 = Legal only
            - None = Semua data (ILLEGAL + LEGAL)
        optimizers (Optional[List[str]]): List of optimizers to test
            - Default: ["sgd", "rmsprop", "adam"]
            - Valid values: "sgd", "rmsprop", "adam"
    """
    is_legal: Optional[int] = None
    optimizers: Optional[List[str]] = None

    def __post_init__(self):
        """Validate request parameters"""

        # Validate is_legal
        if self.is_legal is not None:
            if not isinstance(self.is_legal, int):
                raise ValueError("is_legal must be an integer (0 or 1)")
            if self.is_legal not in [0, 1]:
                raise ValueError("is_legal must be 0 (ILLEGAL) or 1 (LEGAL)")

        # Set default optimizers if not provided
        if self.optimizers is None:
            self.optimizers = ["sgd", "rmsprop", "adam"]

        # Validate optimizers
        if not isinstance(self.optimizers, list):
            raise ValueError("optimizers must be a list of strings")

        if len(self.optimizers) == 0:
            raise ValueError("optimizers must contain at least one value")

        if len(self.optimizers) > 10:
            raise ValueError("optimizers cannot contain more than 10 values")

        # Valid optimizer names
        valid_optimizers = ["sgd", "rmsprop", "adam"]

        # Validate each optimizer
        for optimizer in self.optimizers:
            if not isinstance(optimizer, str):
                raise ValueError(f"optimizer must be a string, got {type(optimizer)}")

            optimizer_lower = optimizer.lower()
            if optimizer_lower not in valid_optimizers:
                raise ValueError(f"optimizer must be one of {valid_optimizers}, got '{optimizer}'")

        # Convert to lowercase and remove duplicates
        self.optimizers = list(set([opt.lower() for opt in self.optimizers]))

        # Sort for consistency
        self.optimizers.sort()
