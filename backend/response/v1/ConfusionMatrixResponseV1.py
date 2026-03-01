from dataclasses import dataclass

@dataclass
class ConfusionMatrixResponseV1:
    """
    Response DTO untuk Confusion Matrix

    Berisi:
    - Confusion Matrix (TP, TN, FP, FN) dengan count dan penjelasan
    - Metrics (Accuracy, Precision, Recall, F1-Score) dengan count dan penjelasan
    - Metadata (total samples, legal count, illegal count)
    """
    # Metadata
    legal_count: int
    illegal_count: int

    # ========== COUNTS (Semua nilai numerik) ==========

    # Total Samples Count
    ts_count: int

    # Confusion Matrix Counts
    tp_count: int           # True Positive Count
    tn_count: int           # True Negative Count
    fp_count: int           # False Positive Count
    fn_count: int           # False Negative Count

    # Metrics Counts
    accuracy_count: float       # Accuracy Value
    precision_count: float      # Precision Value
    recall_count: float         # Recall Value
    f1_score_count: float       # F1-Score Value

    # ========== PENJELASAN (Semua interpretasi) ==========

    # Total Samples Penjelasan
    ts_penjelasan: str

    # Confusion Matrix Penjelasan
    tp_penjelasan: str      # Penjelasan TP
    tn_penjelasan: str      # Penjelasan TN
    fp_penjelasan: str      # Penjelasan FP
    fn_penjelasan: str      # Penjelasan FN

    # Metrics Penjelasan
    accuracy_penjelasan: str    # Penjelasan Accuracy
    precision_penjelasan: str   # Penjelasan Precision
    recall_penjelasan: str      # Penjelasan Recall
    f1_score_penjelasan: str    # Penjelasan F1-Score
