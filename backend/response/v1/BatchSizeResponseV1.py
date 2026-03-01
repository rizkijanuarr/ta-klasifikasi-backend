from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class BatchSizeResponseV1:
    """
    Response DTO untuk Batch Size Evaluation

    Structure:
    {
        "is_legal": 0,
        "keterangan_legal": "Filtered by ILLEGAL",
        "total_samples": 1142,
        "batch_size_results": [
            {
                "batch_size": 16,
                "iterations_per_epoch": 72,
                "last_batch_size": 6,
                "memory_efficiency": "high",
                "speed_category": "fast",
                "convergence_quality": "good"
            },
            ...
        ],
        "comparison": {
            "smallest_batch": {...},
            "largest_batch": {...},
            "recommended_batch": {...}
        },
        "penjelasan": {
            "batch_size_concept": "...",
            "iterations_calculation": "...",
            "trade_offs": "...",
            "recommendation": "..."
        }
    }
    """

    # Filter info
    is_legal: Optional[int]
    keterangan_legal: str
    total_samples: int

    # Batch size results
    batch_size_results: List[Dict]

    # Comparison & analysis
    comparison: Dict

    # Indonesian explanations
    penjelasan: Dict
