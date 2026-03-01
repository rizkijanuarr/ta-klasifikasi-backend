from dataclasses import dataclass
from typing import Optional


@dataclass
class EpochTrainingRequestV1:
    """
    Request DTO untuk Epoch Training (tanpa validation split)

    Endpoint ini untuk training model menggunakan SEMUA data tanpa validation split.
    Cocok untuk final training setelah hyperparameter tuning.

    Attributes:
        is_legal (Optional[int]): Filter data berdasarkan kategori
            - 0 = Illegal only
            - 1 = Legal only
            - None = Semua data (ILLEGAL + LEGAL)
        max_epochs (int): Maximum number of epochs to train
            - Default: 100
            - Range: 1-1000
    """
    is_legal: Optional[int] = None
    max_epochs: int = 100

    def __post_init__(self):
        """Validate request parameters"""

        # Validate is_legal
        if self.is_legal is not None:
            if not isinstance(self.is_legal, int):
                raise ValueError("is_legal must be an integer (0 or 1)")
            if self.is_legal not in [0, 1]:
                raise ValueError("is_legal must be 0 (ILLEGAL) or 1 (LEGAL)")

        # Validate max_epochs
        if not isinstance(self.max_epochs, int):
            raise ValueError("max_epochs must be an integer")

        if self.max_epochs < 1 or self.max_epochs > 1000:
            raise ValueError("max_epochs must be between 1 and 1000")
