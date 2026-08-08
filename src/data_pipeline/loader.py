# Data Pipeline Module for AHRE
# Responsible for loading CERT CSV logs and constructing user behavioral features.

import pandas as pd
import numpy as np

def load_logon_data(filepath):
    """Loads and cleans logon/logoff activity logs."""
    df = pd.read_csv(filepath)
    # Parse timestamps
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df
