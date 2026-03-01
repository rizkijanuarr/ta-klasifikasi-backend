from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class OptimizerResponseV1:
    """
    Response DTO untuk Optimizer Comparison

    Structure:
    {
        "is_legal": 0,
        "keterangan_legal": "Filtered by ILLEGAL",
        "total_samples": 1142,
        "optimizer_results": [
            {
                "optimizer": "sgd",
                "convergence_speed": "slow",
                "final_accuracy": 1.0,
                "stability": "high",
                "learning_rate": 0.01,
                "characteristics": {
                    "pros": [...],
                    "cons": [...]
                }
            },
            ...
        ],
        "comparison": {
            "fastest_convergence": {...},
            "highest_accuracy": {...},
            "most_stable": {...},
            "recommended": {...}
        },
        "penjelasan": {
            "optimizer_concept": "...",
            "sgd_explanation": "...",
            "rmsprop_explanation": "...",
            "adam_explanation": "...",
            "recommendation": "..."
        }
    }
    """

    # Filter info
    is_legal: Optional[int]
    keterangan_legal: str
    total_samples: int

    # Optimizer results
    optimizer_results: List[Dict]

    # Comparison & analysis
    comparison: Dict

    # Indonesian explanations
    penjelasan: Dict
