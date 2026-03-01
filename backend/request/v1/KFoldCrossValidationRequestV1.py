from dataclasses import dataclass
from typing import Optional

@dataclass
class KFoldCrossValidationRequestV1:
    """
    Request DTO untuk K-Fold Cross Validation

    Parameters:
    - is_legal: Filter data (0=illegal, 1=legal, None=all)
    """
    is_legal: Optional[int] = None

    def __post_init__(self):
        # Validate is_legal if provided
        if self.is_legal is not None and self.is_legal not in [0, 1]:
            raise ValueError("is_legal must be 0 (illegal) or 1 (legal)")
