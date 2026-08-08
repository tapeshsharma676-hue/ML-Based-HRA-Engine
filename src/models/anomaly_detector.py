# Anomaly Detection & Risk Scoring Model Module

from sklearn.ensemble import IsolationForest
import numpy as np

class AHREAnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def fit(self, X):
        self.model.fit(X)

    def predict_risk_score(self, X):
        """Converts anomaly decision function into a 0-100 normalized risk score."""
        raw_scores = self.model.decision_function(X) # lower score = more anomalous
        # Normalize to 0-100 scale where 100 = highest risk
        min_s, max_s = raw_scores.min(), raw_scores.max()
        if max_s == min_s:
            return np.zeros(len(X))
        normalized = 100 * (1 - (raw_scores - min_s) / (max_s - min_s))
        return np.round(normalized, 2)
