from dataclasses import dataclass
from typing import Optional

@dataclass
class ConfusionMatrixRequestV1:
    """
    Request DTO untuk mendapatkan Confusion Matrix

    Filter berdasarkan:
    - is_legal: 0 = illegal only, 1 = legal only, None = semua data
    """
    is_legal: Optional[int] = None  # None = semua data, 0 = illegal only, 1 = legal only

    def __post_init__(self):
        """Validasi field"""
        # Validate is_legal if provided
        if self.is_legal is not None and self.is_legal not in [0, 1]:
            raise ValueError("is_legal must be 0 (illegal) or 1 (legal)")
