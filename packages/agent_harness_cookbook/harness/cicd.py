from __future__ import annotations

from typing import Sequence
import math

class EvaluationGate:
    """
    Performs statistical drift analysis comparing new evaluation distributions
    against a golden dataset baseline to block regressive deployments.
    """
    def __init__(self, baseline_scores: Sequence[float]) -> None:
        self.baseline_scores = baseline_scores
        self._baseline_mean = sum(baseline_scores) / len(baseline_scores) if baseline_scores else 0.0

    def evaluate_deployment(self, new_scores: Sequence[float], alpha: float = 0.05) -> tuple[bool, str]:
        """
        Uses a Welch's t-test (simplified) to determine if the new scores are statistically 
        significantly worse than the baseline.
        """
        if not new_scores or not self.baseline_scores:
            return False, "Insufficient data for statistical gating."
            
        new_mean = sum(new_scores) / len(new_scores)
        
        # If the new mean is higher or equal, it's an improvement or neutral. Pass immediately.
        if new_mean >= self._baseline_mean:
             return True, f"Pass: New mean ({new_mean:.3f}) >= baseline ({self._baseline_mean:.3f})"
             
        # Calculate variances
        def variance(data: Sequence[float], mean: float) -> float:
            if len(data) <= 1:
                return 0.0
            return sum((x - mean) ** 2 for x in data) / (len(data) - 1)
            
        var_baseline = variance(self.baseline_scores, self._baseline_mean)
        var_new = variance(new_scores, new_mean)
        
        n_base = len(self.baseline_scores)
        n_new = len(new_scores)
        
        # Calculate t-statistic
        denominator = math.sqrt((var_baseline / n_base) + (var_new / n_new))
        if denominator == 0:
            # Variances are zero, and we know new_mean < baseline_mean
            return False, f"Fail: Absolute regression detected. New ({new_mean}) < Baseline ({self._baseline_mean})"
            
        t_stat = (self._baseline_mean - new_mean) / denominator
        
        # For simplicity in this cookbook, we use a basic heuristic threshold for the t-statistic
        # corresponding roughly to p < 0.05. (e.g., t > 1.96 for large n)
        # In a real system, use scipy.stats.ttest_ind
        critical_value = 1.96 
        
        is_significant_regression = t_stat > critical_value
        
        if is_significant_regression:
            return False, f"Blocked: Statistically significant regression detected. t-stat={t_stat:.2f}"
            
        return True, f"Pass: Regression detected, but it is not statistically significant (noise). t-stat={t_stat:.2f}"
