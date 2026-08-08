"""
AHRE Behavioral Feature Extractor (Member 1 Module)
Aggregates raw CERT activity logs (logon, device, file) into a user-day feature matrix.
"""

import pandas as pd
import numpy as np
import os

def extract_features(raw_data_dir):
    """
    Reads logon.csv, device.csv, file.csv and constructs daily behavioral metrics per user.
    """
    logon_path = os.path.join(raw_data_dir, "logon.csv")
    device_path = os.path.join(raw_data_dir, "device.csv")
    file_path = os.path.join(raw_data_dir, "file.csv")

    features = []

    if os.path.exists(logon_path):
        df_logon = pd.read_csv(logon_path)
        df_logon['date_dt'] = pd.to_datetime(df_logon['date'])
        df_logon['day'] = df_logon['date_dt'].dt.date
        df_logon['hour'] = df_logon['date_dt'].dt.hour

        # Feature 1: Off-hours logins (before 7 AM or after 7 PM)
        df_logon['is_off_hours'] = (df_logon['hour'] < 7) | (df_logon['hour'] > 19)
        # Feature 2: Failed logins
        df_logon['is_failed'] = df_logon['activity'] == 'FailedLogon'

        logon_summary = df_logon.groupby(['user', 'day']).agg(
            total_logons=('activity', 'count'),
            off_hours_logins=('is_off_hours', 'sum'),
            failed_logins=('is_failed', 'sum')
        ).reset_index()
        features.append(logon_summary)

    if os.path.exists(device_path):
        df_device = pd.read_csv(device_path)
        df_device['date_dt'] = pd.to_datetime(df_device['date'])
        df_device['day'] = df_device['date_dt'].dt.date
        df_device['is_connect'] = df_device['activity'] == 'Connect'

        device_summary = df_device.groupby(['user', 'day']).agg(
            usb_connect_count=('is_connect', 'sum')
        ).reset_index()
        features.append(device_summary)

    if os.path.exists(file_path):
        df_file = pd.read_csv(file_path)
        df_file['date_dt'] = pd.to_datetime(df_file['date'])
        df_file['day'] = df_file['date_dt'].dt.date
        df_file['is_copy'] = df_file['activity'] == 'FileCopy'

        file_summary = df_file.groupby(['user', 'day']).agg(
            file_copy_count=('is_copy', 'sum'),
            total_file_access=('activity', 'count')
        ).reset_index()
        features.append(file_summary)

    # Merge all feature tables
    if not features:
        return pd.DataFrame()

    final_df = features[0]
    for feat_df in features[1:]:
        final_df = pd.merge(final_df, feat_df, on=['user', 'day'], how='outer')

    # Fill NaN values with 0
    final_df = final_df.fillna(0)
    
    return final_df

if __name__ == "__main__":
    raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw"))
    proc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/processed"))
    
    os.makedirs(proc_dir, exist_ok=True)
    df_features = extract_features(raw_dir)
    out_path = os.path.join(proc_dir, "user_features.csv")
    df_features.to_csv(out_path, index=False)
    
    print(f"Extracted {len(df_features)} behavioral feature vectors -> Saved to {out_path}")
    print("\nSample Feature Vector:")
    print(df_features.head())
