from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class EpochEarlyStoppingResponseV1:
    """
    Response DTO for Epoch + Early Stopping endpoint

    Contains training simulation results with epoch-by-epoch tracking,
    early stopping information, and performance summary.
    """

    # Filter information
    is_legal: Optional[int]
    keterangan_legal: str

    # Dataset information
    total_samples: int
    train_samples: int
    validation_samples: int

    # Training configuration
    max_epochs: int
    patience: int
    validation_split: float

    # Early stopping information
    early_stopped_at_epoch: int
    best_epoch: int

    # Epoch-by-epoch results
    epochs: List[Dict]

    # Summary metrics
    summary: Dict

    # Explanations in Indonesian
    penjelasan: Dict
