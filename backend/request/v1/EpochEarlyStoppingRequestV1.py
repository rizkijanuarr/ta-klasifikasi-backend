from dataclasses import dataclass
from typing import Optional


@dataclass
class EpochEarlyStoppingRequestV1:
    """
    Request DTO for Epoch + Early Stopping endpoint

    Attributes:
        is_legal (Optional[int]): Filter data by category
            - 0: Illegal only
            - 1: Legal only
            - None: All data
        max_epochs (int): Maximum number of epochs to train (default: 100)
        patience (int): Number of epochs to wait before early stopping (default: 5)
        validation_split (float): Proportion of data for validation (default: 0.2)
    """

    is_legal: Optional[int] = None
    max_epochs: int = 100
    patience: int = 5
    validation_split: float = 0.2

    def __post_init__(self):
        """
        Validate request parameters after initialization

        Raises:
            ValueError: If any parameter is invalid
        """
        # Validate is_legal
        if self.is_legal is not None and self.is_legal not in [0, 1]:
            raise ValueError("is_legal must be 0 (illegal), 1 (legal), or None (all data)")

        # Validate max_epochs
        if not isinstance(self.max_epochs, int):
            raise ValueError("max_epochs must be an integer")
        if self.max_epochs < 1 or self.max_epochs > 1000:
            raise ValueError("max_epochs must be between 1 and 1000")

        # Validate patience
        if not isinstance(self.patience, int):
            raise ValueError("patience must be an integer")
        if self.patience < 1 or self.patience > 50:
            raise ValueError("patience must be between 1 and 50")

        # Validate validation_split
        if not isinstance(self.validation_split, (int, float)):
            raise ValueError("validation_split must be a number")
        if self.validation_split < 0.1 or self.validation_split > 0.5:
            raise ValueError("validation_split must be between 0.1 and 0.5 (10%-50%)")

        # Ensure validation_split is float
        self.validation_split = float(self.validation_split)
