"""
AHRE Risk Scoring Engine & Anomaly Detector (Member 2 Module)
Computes dynamic 0-100 risk score and provides feature-level risk explanations.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os

class AHRERiskScorer:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.feature_cols = [
            'off_hours_logins', 'failed_logins', 'usb_connect_count', 
            'file_copy_count', 'total_file_access'
        ]

    def fit_predict(self, df):
        """Fits Isolation Forest and appends 'risk_score' and 'risk_category' to DataFrame."""
        X = df[self.feature_cols].fillna(0)
        self.model.fit(X)
        
        # Decision function gives negative values for anomalies, positive for normal
        decision_scores = self.model.decision_function(X)
        
        # Transform decision scores to 0-100 Risk Scale
        # Lower decision score -> Higher Risk
        min_s, max_s = decision_scores.min(), decision_scores.max()
        if max_s == min_s:
            risk_scores = np.zeros(len(df))
        else:
            # Min-Max Scaling to 0 - 100
            risk_scores = 100 * (1 - (decision_scores - min_s) / (max_s - min_s))

        df['risk_score'] = np.round(risk_scores, 2)
        
        # Assign Risk Category
        def categorize(score):
            if score >= 75:
                return 'CRITICAL'
            elif score >= 50:
                return 'HIGH'
            elif score >= 25:
                return 'MEDIUM'
            else:
                return 'LOW'
                
        df['risk_category'] = df['risk_score'].apply(categorize)
        
        # Generate Top Risk Factors (Explainability Layer)
        df['explanation'] = df.apply(self._generate_explanation, axis=1)
        
        return df

    def _generate_explanation(self, row):
        """Rule-augmented Explainability Layer for Score Spikes."""
        reasons = []
        if row.get('failed_logins', 0) > 0:
            reasons.append(f"{int(row['failed_logins'])} Failed Logins")
        if row.get('off_hours_logins', 0) > 0:
            reasons.append(f"{int(row['off_hours_logins'])} Off-Hours Logins")
        if row.get('usb_connect_count', 0) > 0:
            reasons.append(f"{int(row['usb_connect_count'])} USB Connections")
        if row.get('file_copy_count', 0) > 0:
            reasons.append(f"{int(row['file_copy_count'])} File Copy Activity")

        if not reasons:
            return "Normal baseline activity"
        return "Anomaly detected due to: " + ", ".join(reasons)

if __name__ == "__main__":
    processed_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed/user_features.csv"))
    
    if os.path.exists(processed_file):
        df_features = pd.read_csv(processed_file)
        scorer = AHRERiskScorer()
        df_results = scorer.fit_predict(df_features)
        
        output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed/user_risk_scores.csv"))
        df_results.to_csv(output_path, index=False)
        
        print(f"Risk Scores calculated -> Saved to {output_path}")
        print("\nTop High Risk Anomalies Detected:")
        print(df_results.sort_values(by='risk_score', ascending=False)[['user', 'day', 'risk_score', 'risk_category', 'explanation']].head(10))
    else:
        print("Feature file user_features.csv not found! Run feature_extractor.py first.")
