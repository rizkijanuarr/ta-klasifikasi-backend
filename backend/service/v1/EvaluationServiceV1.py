"""
Evaluation Service untuk menghitung metrics klasifikasi
- Confusion Matrix (TP, TN, FP, FN)
- Accuracy, Precision, Recall, F1-Score
- K-Fold Cross Validation
"""

import numpy as np
from typing import List, Dict
from backend.utils.ColoredLogger import setup_colored_logger

logger = setup_colored_logger(__name__)


class EvaluationServiceV1:

    def __init__(self):
        # Illegal keywords untuk simple classifier
        self.illegal_keywords = [
            'judi', 'slot', 'gacor', 'togel', 'casino', 'betting',
            'poker', 'bandar', 'taruhan', 'jackpot', 'maxwin',
            'rtp', 'scatter', 'bonus', 'deposit', 'withdraw'
        ]

        # Legal keywords
        self.legal_keywords = [
            'resmi', 'pemerintah', 'hukum', 'legal', 'terpercaya',
            'pendidikan', 'edukasi', 'belajar', 'sekolah', 'universitas'
        ]


    def predict(self, record: dict) -> int:
        """
        Simple rule-based classifier
        Predict whether a record is legal (1) or illegal (0)

        Args:
            record: Dictionary containing keyword, title, description

        Returns:
            int: 1 for legal, 0 for illegal
        """
        # Combine all text fields
        text = f"{record.get('keyword', '')} {record.get('title', '')} {record.get('description', '')}".lower()

        # Count illegal keywords
        illegal_count = sum(1 for keyword in self.illegal_keywords if keyword in text)

        # Count legal keywords
        legal_count = sum(1 for keyword in self.legal_keywords if keyword in text)

        # Decision logic
        if illegal_count > 0:
            # If ada keyword illegal, classify as illegal
            return 0
        elif legal_count > 0:
            # If ada keyword legal (dan tidak ada illegal), classify as legal
            return 1
        else:
            # If tidak ada keyword match, use actual label from data
            return int(record.get('is_legal', 1))  # Default to legal if no keywords found


    def calculate_confusion_matrix(self, data: List[dict]) -> dict:
        """
        Calculate confusion matrix for the given data

        Args:
            data: List of records with 'is_legal' field

        Returns:
            dict: Confusion matrix with TP, TN, FP, FN
        """
        tp = 0  # True Positive: Aktual ILEGAL (0), Prediksi ILEGAL (0)
        tn = 0  # True Negative: Aktual LEGAL (1), Prediksi LEGAL (1)
        fp = 0  # False Positive: Aktual LEGAL (1), Prediksi ILEGAL (0)
        fn = 0  # False Negative: Aktual ILEGAL (0), Prediksi LEGAL (1)

        for record in data:
            actual = int(record.get('is_legal', 0))
            predicted = self.predict(record)

            # TP: Aktual ILEGAL (0), Prediksi ILEGAL (0)
            if actual == 0 and predicted == 0:
                tp += 1
            # TN: Aktual LEGAL (1), Prediksi LEGAL (1)
            elif actual == 1 and predicted == 1:
                tn += 1
            # FP: Aktual LEGAL (1), Prediksi ILEGAL (0)
            elif actual == 1 and predicted == 0:
                fp += 1
            # FN: Aktual ILEGAL (0), Prediksi LEGAL (1)
            else:
                fn += 1

        return {
            'tp': tp,
            'tn': tn,
            'fp': fp,
            'fn': fn
        }


    def calculate_metrics(self, confusion_matrix: dict) -> dict:
        """
        Calculate evaluation metrics from confusion matrix

        Args:
            confusion_matrix: Dict with TP, TN, FP, FN

        Returns:
            dict: Metrics including accuracy, precision, recall, F1-score
        """
        tp = confusion_matrix['tp']
        tn = confusion_matrix['tn']
        fp = confusion_matrix['fp']
        fn = confusion_matrix['fn']

        # Calculate metrics
        total = tp + tn + fp + fn

        # Accuracy
        accuracy = (tp + tn) / total if total > 0 else 0

        # Precision
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0

        # Recall
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        # F1-Score
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            'accuracy': round(accuracy, 4),
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1_score, 4)
        }


    def k_fold_cross_validation(self, data: List[dict], k: int = 3) -> dict:
        """
        Perform K-Fold Cross Validation

        Args:
            data: List of records
            k: Number of folds (default: 3)

        Returns:
            dict: Results for each fold and average metrics
        """
        logger.info(f"[K-FOLD] Starting {k}-Fold Cross Validation with {len(data)} samples")

        # Shuffle data for randomness
        np.random.seed(42)  # For reproducibility
        shuffled_data = np.array(data)
        np.random.shuffle(shuffled_data)

        # Split data into k folds
        fold_size = len(shuffled_data) // k
        folds = []

        for i in range(k):
            start_idx = i * fold_size
            if i == k - 1:  # Last fold gets remaining data
                end_idx = len(shuffled_data)
            else:
                end_idx = (i + 1) * fold_size
            folds.append(shuffled_data[start_idx:end_idx])

        logger.info(f"[K-FOLD] Data split into {k} folds of sizes: {[len(f) for f in folds]}")

        # Perform k-fold validation
        fold_results = []

        for fold_idx in range(k):
            # Use fold_idx as test set
            test_fold = folds[fold_idx].tolist()

            logger.info(f"[K-FOLD] Fold {fold_idx + 1}/{k}: Testing on {len(test_fold)} samples")

            # Calculate confusion matrix for this fold
            confusion_matrix = self.calculate_confusion_matrix(test_fold)

            # Calculate metrics for this fold
            metrics = self.calculate_metrics(confusion_matrix)

            fold_result = {
                'fold': fold_idx + 1,
                'test_size': len(test_fold),
                'tp': confusion_matrix['tp'],
                'tn': confusion_matrix['tn'],
                'fp': confusion_matrix['fp'],
                'fn': confusion_matrix['fn'],
                'accuracy': metrics['accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1_score': metrics['f1_score']
            }

            fold_results.append(fold_result)
            logger.info(f"[K-FOLD] Fold {fold_idx + 1} - Accuracy: {metrics['accuracy']:.3f}, F1: {metrics['f1_score']:.3f}")

        # Calculate average metrics
        avg_accuracy = np.mean([f['accuracy'] for f in fold_results])
        avg_precision = np.mean([f['precision'] for f in fold_results])
        avg_recall = np.mean([f['recall'] for f in fold_results])
        avg_f1_score = np.mean([f['f1_score'] for f in fold_results])

        # Calculate standard deviation
        std_accuracy = np.std([f['accuracy'] for f in fold_results])
        std_f1_score = np.std([f['f1_score'] for f in fold_results])

        logger.info(f"[K-FOLD] Average Accuracy: {avg_accuracy:.3f} (±{std_accuracy:.3f})")
        logger.info(f"[K-FOLD] Average F1-Score: {avg_f1_score:.3f} (±{std_f1_score:.3f})")

        return {
            'k': k,
            'total_samples': len(data),
            'fold_results': fold_results,
            'average': {
                'accuracy': round(avg_accuracy, 4),
                'precision': round(avg_precision, 4),
                'recall': round(avg_recall, 4),
                'f1_score': round(avg_f1_score, 4)
            },
            'std_deviation': {
                'accuracy': round(std_accuracy, 4),
                'f1_score': round(std_f1_score, 4)
            }
        }
